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


class Exchange(BaseModel):
    """Describes the fields and attributes of the Exchange model in the database."""

    from_cur = models.ForeignKey(to="Currency", on_delete=models.CASCADE, related_name="exch_from")
    to_cur = models.ForeignKey(to="Currency", on_delete=models.CASCADE, related_name="exch_to")
    value = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return f"{str(self.from_cur)} -> {str(self.to_cur)}: {str(self.value)}"

    class Mete:
        """Describes class metadata."""

        db_table = "exchanges"
