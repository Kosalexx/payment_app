from dataclasses import dataclass
from decimal import Decimal

from django.core.files.uploadedfile import InMemoryUploadedFile
from shop.models import Item, Order, OrderItem


@dataclass
class AddItemDTO:
    name: str
    price: Decimal
    description: str | None
    currency: str
    photo: InMemoryUploadedFile | None
    category: str


@dataclass
class OrderItemDTO:
    item: Item
    qty: int


@dataclass
class OrderDTO:
    user_email: str
    coupon: str | None
    items: list[OrderItemDTO] | None
    currency: str


@dataclass
class OrderDataDTO:
    total_by_cur: list[tuple[str, Decimal]]
    order: Order
    order_items: list[OrderItem]
    total_in_order_cur: Decimal
    final_total: Decimal
