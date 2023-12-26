from typing import Any

from django.db import migrations
from shop.models import Category, Tax

a = (
    "food_tax" "cloth_tax",
    "electronics_tax",
    "furniture_tax",
    "sport_goods_tax",
    "other_goods_tax",
    "sales_stripe_tax",
)


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""

    food_tax = Tax.objects.get(name="food_tax")
    cloth_tax = Tax.objects.get(name="cloth_tax")
    electronics_tax = Tax.objects.get(name="electronics_tax")
    furniture_tax = Tax.objects.get(name="furniture_tax")
    sport_goods_tax = Tax.objects.get(name="sport_goods_tax")
    other_goods_tax = Tax.objects.get(name="other_goods_tax")

    default_values = (
        ("food", "Foodstuff", food_tax),
        ("cloth", "Clothing and footwear (excluding sportswear)", cloth_tax),
        ("electronics", "Household appliances and electronics", electronics_tax),
        ("electronics", "Household appliances and electronics", electronics_tax),
        ("furniture", "Home and garden furniture", furniture_tax),
        ("sportswear", "Sportswear and shoes for sport", sport_goods_tax),
        ("other", "other goods", other_goods_tax),
    )
    categories_list = [Category(name=name, description=desc, tax=tax) for name, desc, tax in default_values]
    Category.objects.bulk_create(categories_list, ignore_conflicts=True)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    Category.objects.raw("TRUNCATE TABLE categories;")


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("shop", "0005_populate_tax_table_by_default_values"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
