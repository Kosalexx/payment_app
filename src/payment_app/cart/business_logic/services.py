from django.db.models import QuerySet
from shop.models import Item


def get_cart_products_list(product_ids: list[str]) -> QuerySet:
    """Retrieves product information from the database for use in the shopping cart."""

    products = Item.objects.select_related("currency").filter(id__in=product_ids)
    return products
