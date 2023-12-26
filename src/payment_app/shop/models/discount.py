from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseModel


class Discount(BaseModel):
    """Describes the fields and attributes of the Discount model in the database."""

    name = models.CharField(max_length=30, unique=True)
    percent_off = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], default=0)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return f"{str(self.name)} is {self.percent_off}%"

    class Meta:
        """Describes class metadata."""

        db_table = "discounts"
