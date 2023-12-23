from django.http import HttpRequest

from .cart import Cart


def cart(request: HttpRequest) -> dict:
    """Cart context processor."""

    return {"cart": Cart(request)}
