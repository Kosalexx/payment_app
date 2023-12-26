from shop.models import Currency, Item


def get_currencies_func() -> list[tuple[str, str]]:
    """Gets currency info from DB to AddItemForm."""

    currencies = [
        ("", ""),
    ] + [(cur.name, cur.name) for cur in Currency.objects.all().order_by("-created_at")]
    return currencies


def get_currencies_names_from_items(items: list[Item]) -> list[tuple[str, str]]:
    """Gets currency info."""

    currencies = []
    for item in items:
        cur_name = item.currency.name
        currencies.append((cur_name, cur_name))
    return currencies
