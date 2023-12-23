"""
Custom migration that populate NotificationType table with default values.
"""

from typing import Any

from django.db import migrations
from shop.models import Currency

DEFAULT_VALUES = ("usd", "eur")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    currencies_list = [Currency(name=cur) for cur in DEFAULT_VALUES]
    Currency.objects.bulk_create(currencies_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    Currency.objects.raw("TRUNCATE TABLE notification_types")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
