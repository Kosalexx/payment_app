from shop.models import Category


def get_categories_func() -> list[tuple[str, str]]:
    """Gets category info from DB to AddItemForm."""

    categories = [(cat.name, cat.name) for cat in Category.objects.all().order_by("-created_at")]
    return categories
