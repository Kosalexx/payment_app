from django.db import models

from .base import BaseModel


class Currency(BaseModel):
    """Describes the fields and attributes of the Currency model in the database."""

    name = models.CharField(max_length=10, default="USD")

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        """Describes class metadata."""

        db_table = "currencies"
