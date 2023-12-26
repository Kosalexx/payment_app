from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseModel


class Tax(BaseModel):
    """Describes the fields and attributes of the Tax model in the database."""

    percentage = models.DecimalField(
        decimal_places=2, max_digits=9, validators=[MaxValueValidator(Decimal(99)), MinValueValidator(0)], default=0
    )
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f"{(self.name)}: {self.percentage}%"

    class Meta:
        """Describes class metadata."""

        db_table = "taxes"
