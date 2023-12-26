import logging
from decimal import Decimal

from cart.business_logic.errors import EmptyCartError
from cart.cart import Cart
from django.db import transaction
from payment.business_logic.services import convert_price, get_stripe_payment_tax
from shop.business_logic.dto import OrderDataDTO, OrderDTO, OrderItemDTO
from shop.business_logic.errors import DiscountNotFoundError, ItemNotFoundError
from shop.models import Currency, Order, OrderItem

from .discount import get_discount_by_name
from .item import get_product_by_id

logger = logging.getLogger(__name__)


def create_order_item_dto_by_item_id(item_id: int, qty: int | None = None) -> OrderItemDTO:
    """Creates OrderItemDTO by passed item_id."""

    try:
        item = get_product_by_id(item_id=item_id)
        quantity = 1 if not qty else qty
        dto = OrderItemDTO(item=item, qty=quantity)
        return dto
    except ItemNotFoundError:
        raise ItemNotFoundError("Item with provided data not found.")


def create_order(order_dto: OrderDTO) -> int:
    """Creates order in the database and returns Order object."""

    with transaction.atomic():
        currency = Currency.objects.get(name=order_dto.currency)
        order = Order.objects.create(customer_email=order_dto.user_email, payment_currency=currency)
        order_items_list = []
        if order_dto.coupon:
            try:
                discount = get_discount_by_name(name=order_dto.coupon)
                order.discount = discount
                order.save()
            except DiscountNotFoundError:
                logger.info("Discount with provided data not found.", extra={"entered_coupon": order_dto.coupon})
        if order_dto.items:
            for item_dto in order_dto.items:
                order_item = OrderItem(order=order, item=item_dto.item, quantity=item_dto.qty)
                order_items_list.append(order_item)
        sales_tax_from_db = get_stripe_payment_tax()  # addition Stripe sales tax to order(6%).
        # In the future, we can invent another system to add taxes to the order depending on some parameters.
        order.tax.set(
            [
                sales_tax_from_db,
            ]
        )
        OrderItem.objects.bulk_create(order_items_list, ignore_conflicts=True)
    return int(order.pk)


def get_items_dto_list_by_cart(cart: Cart) -> list[OrderItemDTO]:
    """Parses product info from the shopping cart and creates list of OrderItemDTO."""

    result_list: list[OrderItemDTO] = []
    for item in cart:
        item_obj = item["product"]
        qty = item["qty"]
        dto = OrderItemDTO(item=item_obj, qty=qty)
        result_list.append(dto)
    if result_list != []:
        return result_list
    else:
        raise EmptyCartError


def get_order_info_by_id(order_id: int) -> OrderDataDTO:
    """Gets full order info form DB."""

    order = Order.objects.select_related("payment_currency", "discount").prefetch_related("tax").get(pk=order_id)

    total_price_by_currency: dict[str, Decimal] = {}
    order_items = OrderItem.objects.select_related(
        "item", "item__currency", "item__category", "item__category__tax", "order", "order__discount"
    ).filter(order=order)

    total_in_order_cur_no_tax_no_disc = Decimal(0)
    total_in_order_cur_with_tax_and_disc = Decimal(0)
    for item in order_items:
        counted_price = Decimal(item.item.price) * item.quantity
        counted_price_with_discount = (
            counted_price
            if order.discount is None
            else (counted_price - (counted_price * order.discount.percent_off / 100))
        )
        counted_price_with_taxes = counted_price_with_discount + (
            (counted_price_with_discount * item.item.category.tax.percentage / 100)
        )
        for tax in order.tax.all():
            counted_price_with_taxes = counted_price_with_taxes + (counted_price_with_discount * tax.percentage / 100)
        total_price_by_currency[item.item.currency.name] = (
            total_price_by_currency.setdefault(item.item.currency.name, Decimal(0)) + counted_price
        )
        if item.item.currency == order.payment_currency:
            total_in_order_cur_no_tax_no_disc += counted_price
            total_in_order_cur_with_tax_and_disc += counted_price_with_taxes
        else:
            total_in_order_cur_no_tax_no_disc += convert_price(
                from_cur=item.item.currency, to_cur=order.payment_currency, price=counted_price
            )
            total_in_order_cur_with_tax_and_disc += convert_price(
                from_cur=item.item.currency, to_cur=order.payment_currency, price=counted_price_with_taxes
            )

    result = OrderDataDTO(
        total_by_cur=list(total_price_by_currency.items()),
        order=order,
        order_items=list(order_items),
        total_in_order_cur=total_in_order_cur_no_tax_no_disc.quantize(Decimal("1.00")),
        final_total=total_in_order_cur_with_tax_and_disc.quantize(Decimal("1.00")),
    )
    return result
