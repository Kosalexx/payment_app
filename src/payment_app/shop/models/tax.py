from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseModel


class Tax(BaseModel):
    """Describes the fields and attributes of the Tax model in the database."""

    value = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0)], default=0)
    name = models.CharField(max_length=30, unique=True)
    stripe_id = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{(self.name)}: {self.value}%"

    class Meta:
        """Describes class metadata."""

        db_table = "taxes"
