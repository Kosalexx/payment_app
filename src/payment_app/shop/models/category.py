from django.db import models

from .base import BaseModel


class Category(BaseModel):
    """Describes fields and attributes of Category model in the database."""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    tax = models.ForeignKey(to="Tax", on_delete=models.SET_DEFAULT, default=None)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        """Describes model metadata."""

        db_table = "categories"
