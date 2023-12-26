from shop.business_logic.errors import DiscountNotFoundError
from shop.models import Discount


def get_discounts_list() -> list[Discount]:
    """Returns data about all discounts in the database."""

    discounts_list = Discount.objects.all()
    return list(discounts_list)


def get_discount_by_name(name: str) -> Discount:
    """Gets discount object by passed discount name."""

    try:
        discount: Discount = Discount.objects.get(name=name.upper())
        return discount

    except Discount.DoesNotExist:
        raise DiscountNotFoundError
