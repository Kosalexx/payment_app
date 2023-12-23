from decimal import Decimal
from typing import Generator

from cart.business_logic.services import get_cart_products_list
from django.conf import settings
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

    def add(self, product: Item, quantity: str) -> None:
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"qty": quantity, "price": str(product.price)}
        self.cart[product_id]["qty"] = quantity
        self.session.modified = True

    def delete(self, product: Item) -> None:
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product: Item, quantity: str) -> None:
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = quantity
            self.session.modified = True

    def get_total_price(self) -> Decimal:
        result: Decimal = sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
        return result

    def clear(self) -> None:
        del self.session[settings.CART_SESSION_ID]
