from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from .base import BaseModel


def item_photo_directory_path(instance: "Item", filename: str) -> str:
    """Provides a path to directory with files of user."""

    return f"items_media/{instance.name}/{filename}"


class Item(BaseModel):
    """Describes the fields and attributes of the Item model in the database."""

    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    photo = models.ImageField(upload_to=item_photo_directory_path, null=True, blank=True)
    currency = models.ForeignKey(to="Currency", on_delete=models.CASCADE, related_name="items")
    price = models.DecimalField(
        default=0, max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal("0.50"))]
    )
    category = models.ForeignKey(to="Category", default=None, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Gets Item absolute url."""
        result = reverse("item-info", args=[self.pk])
        return str(result)

    class Meta:
        """Describes class metadata."""

        db_table = "items"
