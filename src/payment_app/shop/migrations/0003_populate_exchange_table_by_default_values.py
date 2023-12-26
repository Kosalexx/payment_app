from decimal import Decimal
from typing import Any

from django.db import migrations
from shop.models import Currency, Exchange


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""

    usd_cur = Currency.objects.get(name="usd")
    eur_cur = Currency.objects.get(name="eur")
    default_values = ((usd_cur, eur_cur, Decimal(0.91)), (eur_cur, usd_cur, Decimal(1.10)))
    exchanges_list = [Exchange(from_cur=fr, to_cur=to, value=val) for fr, to, val in default_values]
    Exchange.objects.bulk_create(exchanges_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    Exchange.objects.raw("TRUNCATE TABLE exchanges;")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("shop", "0002_populate_currency_table_by_default_values"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
