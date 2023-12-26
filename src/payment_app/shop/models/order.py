from django.db import models

from .base import BaseModel


class Order(BaseModel):
    """Describes the fields and attributes of the Order model in the database."""

    items = models.ManyToManyField(to="Item", through="OrderItem", related_name="item_order")
    paid = models.BooleanField(default=False)
    customer_email = models.EmailField(default="unknown@gmail.com")
    discount = models.ForeignKey(to="Discount", null=True, default=None, on_delete=models.SET_DEFAULT)
    payment_currency = models.ForeignKey(to="Currency", on_delete=models.CASCADE, related_name="orders")
    tax = models.ManyToManyField(to="Tax", db_table="order_taxes", related_name="orders")

    def __str__(self) -> str:
        return f"Order_{self.pk}"

    class Meta:
        """Describes class metadata."""

        db_table = "orders"
