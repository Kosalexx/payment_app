from django.db import models

from .base import BaseModel


class OrderItem(BaseModel):
    """Describes the fields and attributes of the OrderItem model in the database."""

    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="item_order")
    item = models.ForeignKey(to="Item", on_delete=models.CASCADE, related_name="order_item")
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        """Describes class metadata."""

        db_table = "order_items"
        unique_together = [["order", "item"]]
