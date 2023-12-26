from typing import Any

from django.db import migrations
from shop.models import Discount

DEFAULT_VALUES = (
    ("SIMPLE_SOLUTIONS", 50, "Employees only."),
    ("CHRISTMAS_2024", 24, "Hurry up to take advantage of the discount on Christmas and New Year’s Eve holidays!"),
)


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""

    discounts_list = [Discount(name=name, percent_off=value, description=desc) for name, value, desc in DEFAULT_VALUES]
    Discount.objects.bulk_create(discounts_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    Discount.objects.raw("TRUNCATE TABLE discounts;")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("shop", "0003_populate_exchange_table_by_default_values"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
