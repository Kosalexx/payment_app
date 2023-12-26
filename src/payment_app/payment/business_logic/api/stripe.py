from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import stripe
from django.conf import settings
from django.urls import reverse
from payment.business_logic.services import convert_price

if TYPE_CHECKING:
    from django.http import HttpRequest
    from shop.business_logic.dto import OrderDataDTO
    from shop.models import Tax
    from stripe import PaymentIntent
    from stripe.checkout import Session


def create_order_data(data: OrderDataDTO) -> list:
    """Creates product data."""

    domain = settings.DOMAIN
    result = []
    order_currency = data.order.payment_currency
    order_taxes_ids_list = []
    for tax in data.order.tax.all():
        converted_tax_name = tax.name.replace("_", " ").capitalize()
        tax_rate_stripe = stripe.TaxRate.create(
            display_name=converted_tax_name,
            inclusive=False,
            percentage=tax.percentage,
        )
        order_taxes_ids_list.append(tax_rate_stripe.id)
    for item in data.order_items:
        photo_url = (
            [
                (domain + item.item.photo.url),
            ]
            if item.item.photo
            else []
        )
        if item.item.currency != order_currency:
            price = convert_price(from_cur=item.item.currency, to_cur=order_currency, price=item.item.price)
        else:
            price = item.item.price
        specific_product_taxes = order_taxes_ids_list[:]
        tax_from_db: Tax = item.item.category.tax
        converted_tax_name = tax_from_db.name.replace("_", " ").capitalize()
        tax_rate_stripe = stripe.TaxRate.create(
            display_name=converted_tax_name,
            inclusive=False,
            percentage=tax_from_db.percentage,
        )
        specific_product_taxes.append(tax_rate_stripe.id)
        product_data = {
            "price_data": {
                "unit_amount_decimal": (price.quantize(Decimal("1.00")) * Decimal(100)),
                "currency": order_currency,
                "product_data": {
                    "name": item.item.name,
                    "description": item.item.description,
                    "images": photo_url,  # works incorrectly on localhost!
                },
            },
            "quantity": item.quantity,
            "tax_rates": specific_product_taxes,
        }
        result.append(product_data)
    return result


def get_stripe_settings_by_currency_name(cur_name: str) -> dict[str, str]:
    """Gets Stripe SK value by passer cur_name."""
    if cur_name.upper() == "USD":
        return {"secretKey": settings.STRIPE_SECRET_KEY_USD, "publishableKey": settings.STRIPE_PUBLISHABLE_KEY_USD}
    if cur_name.upper() == "EUR":
        return {"secretKey": settings.STRIPE_SECRET_KEY_EUR, "publishableKey": settings.STRIPE_PUBLISHABLE_KEY_EUR}
    return {"secretKey": "ERROR", "publishableKey": "ERROR"}


def create_checkout_session(request: HttpRequest, data: OrderDataDTO) -> Session:
    """Creates stripe checkout session."""
    try:
        keys: dict = get_stripe_settings_by_currency_name(data.order.payment_currency.name)
        stripe.api_key = keys["secretKey"]
        if data.order.discount:
            coupon = stripe.Coupon.create(
                percent_off=data.order.discount.percent_off,
                duration="once",
            )
        checkout_session = stripe.checkout.Session.create(
            line_items=create_order_data(data=data),
            mode="payment",
            customer_email=data.order.customer_email,
            currency=data.order.payment_currency.name,
            discounts=[{"coupon": coupon.id}] if data.order.discount else None,
            tax_id_collection={"enabled": True},
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("failed")),
            metadata={"order_id": data.order.pk},
        )
        return checkout_session
    except Exception as e:
        raise Exception from e


def create_payment_intent(data: OrderDataDTO) -> PaymentIntent:
    """Creates Stripe payment intent."""

    try:
        keys: dict = get_stripe_settings_by_currency_name(data.order.payment_currency.name)
        stripe.api_key = keys["secretKey"]
        customer = stripe.Customer.create(email=data.order.customer_email)
        order_id = data.order.pk
        price = Decimal(data.final_total) * (100)
        intent = stripe.PaymentIntent.create(
            amount=Decimal(price).quantize(Decimal("1")),
            currency=data.order.payment_currency.name,
            payment_method_types=["card"],
            customer=customer["id"],
            metadata={"product_id": order_id},
        )
        return intent
    except Exception as e:
        raise Exception from e
