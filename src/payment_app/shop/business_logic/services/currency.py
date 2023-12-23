from shop.models import Currency


def get_currencies_func() -> list[tuple[str, str]]:
    """Gets currency info from DB to AddItemForm."""

    currencies = [
        ("", ""),
    ] + [(cur.name, cur.name) for cur in Currency.objects.all().order_by("-created_at")]
    return currencies
