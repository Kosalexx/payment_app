from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import stripe
from django.conf import settings
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpRequest
    from shop.models import Item
    from stripe.checkout import Session


def create_product_data(data: Item) -> list:
    """Creates product data."""

    domain = settings.DOMAIN
    result = []
    photo_url = (
        [
            (domain + data.photo.url),
        ]
        if data.photo
        else []
    )
    product_data = {
        "price_data": {
            "unit_amount_decimal": (data.price * Decimal(100)),
            "currency": data.currency.name,
            "product_data": {
                "name": data.name,
                "description": data.description,
                "images": photo_url,  # works incorrectly on localhost!
            },
        },
        "quantity": 1,
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


def create_checkout_session(request: HttpRequest, data: Item) -> Session:
    """Creates stripe checkout session."""
    try:
        keys: dict = get_stripe_settings_by_currency_name(data.currency.name)
        stripe.api_key = keys["secretKey"]
        checkout_session = stripe.checkout.Session.create(
            line_items=create_product_data(data=data),
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("failed")),
        )
        return checkout_session
    except Exception as e:
        raise Exception from e
