from decimal import Decimal

from shop.models import Currency, Exchange


def convert_price(from_cur: Currency, to_cur: Currency, price: Decimal) -> Decimal:
    """Converts price to different currency."""

    exch = Exchange.objects.select_related("from_cur", "to_cur").get(from_cur=from_cur, to_cur=to_cur)
    exch_rate = exch.value
    result_price: Decimal = price * exch_rate
    return result_price
