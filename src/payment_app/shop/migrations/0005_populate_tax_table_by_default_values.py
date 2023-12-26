from decimal import Decimal
from typing import Any

from django.db import migrations
from shop.models import Tax

DEFAULT_VALUES = (
    ("food_tax", Decimal(2.3)),
    ("cloth_tax", Decimal(3.5)),
    ("electronics_tax", Decimal(4.3)),
    ("furniture_tax", Decimal(4.6)),
    ("sport_goods_tax", Decimal(3.6)),
    ("other_goods_tax", Decimal(3.6)),
    ("sales_stripe_tax", Decimal(6)),
)


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""

    taxes_list = [Tax(name=name, percentage=value) for name, value in DEFAULT_VALUES]
    Tax.objects.bulk_create(taxes_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    Tax.objects.raw("TRUNCATE TABLE taxes;")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("shop", "0004_populate_discounts_table_by_default_values"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
