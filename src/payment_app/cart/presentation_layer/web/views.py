from __future__ import annotations

from typing import TYPE_CHECKING

from cart.cart import Cart
from django.http import JsonResponse
from django.shortcuts import redirect, render
from shop.business_logic.services import get_product_by_id

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def cart_view(request: HttpRequest) -> HttpResponse:
    """Shopping cart display controller."""
    cart = Cart(request)

    context = {"cart": cart}

    return render(request, "cart-view.html", context)


def cart_add(request: HttpRequest) -> JsonResponse:
    """Controller for adding a new item to the cart."""
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_product_by_id(item_id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty, "product": product.name})
        return response


def cart_delete(request: HttpRequest) -> JsonResponse:
    """Controller for deleting item from the cart."""

    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        return response


def cart_update(request: HttpRequest) -> JsonResponse:
    """Controller for updating the quantity of products in the cart."""

    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))

        cart.update(product=product_id, quantity=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        return response


def clear_cart(request: HttpRequest) -> HttpResponse:
    """Controller for deleting all items from the cart."""

    cart = Cart(request)
    cart.clear()

    return redirect(to="cart-view")
