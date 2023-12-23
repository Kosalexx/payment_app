from decimal import Decimal
from typing import Generator

from cart.business_logic.services import get_cart_products_list
from django.http import HttpRequest
from shop.models import Item


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get("session_key")
        if not cart:
            cart = self.session["session_key"] = {}
        self.cart = cart

    def __len__(self) -> int:
        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self) -> Generator:
        product_ids = self.cart.keys()
        products = get_cart_products_list(product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]
            yield item

    def add(self, product: Item, quantity: int) -> None:
        """Adds a new item to the cart."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "qty": quantity,
                "price": str(product.price),
                "currency": str(product.currency.name),
            }
        self.cart[product_id]["qty"] = quantity
        self.session.modified = True

    def delete(self, product: int) -> None:
        """Deletes item from the cart by passed product id."""

        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product: int, quantity: int) -> None:
        """Updates item quantity in the cart by passed product id and new quantity value."""

        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = quantity
            self.session.modified = True

    def get_total_price(self) -> dict[str, Decimal]:
        """Gets the cart's total price grouped by currency."""

        total_usd = Decimal(0)
        total_eur = Decimal(0)
        for item in self.cart.values():
            if item["product"].currency.name == "usd":
                total_usd += Decimal(item["price"]) * int(item["qty"])
            else:
                total_eur += Decimal(item["price"]) * int(item["qty"])
        result = {"usd": total_usd, "eur": total_eur}
        return result

    def clear(self) -> None:
        """Clears cart."""

        del self.session["session_key"]
        self.session.modified = True
