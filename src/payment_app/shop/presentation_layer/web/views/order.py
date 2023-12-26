from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cart.business_logic.errors import EmptyCartError
from cart.cart import Cart
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from shop.business_logic.dto import OrderDTO
from shop.business_logic.errors import ItemNotFoundError
from shop.business_logic.services import (
    create_order,
    create_order_item_dto_by_item_id,
    get_currencies_names_from_items,
    get_items_dto_list_by_cart,
    get_order_info_by_id,
    get_product_by_id,
)
from shop.presentation_layer.common.converters import convert_data_from_request_to_dto
from shop.presentation_layer.web.forms import SubmitOrderForm

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def order_create_from_cart_controller(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    try:
        order_items_list = get_items_dto_list_by_cart(cart=cart)
        items_list = [item.item for item in order_items_list]
        currencies = get_currencies_names_from_items(items_list)
    except EmptyCartError:
        return HttpResponseBadRequest("You can't create order with empty cart.")

    if request.method == "GET":
        form = SubmitOrderForm(currencies=currencies)
        context = {"cart": cart, "form": form}
        return render(request=request, template_name="order_create.html", context=context)
    elif request.method == "POST":
        form = SubmitOrderForm(currencies, request.POST)
        if form.is_valid():
            order_data = convert_data_from_request_to_dto(dto=OrderDTO, data_from_request=form.cleaned_data)
            cart.clear()
            order_data.items = order_items_list
            order_id = create_order(order_dto=order_data)
            full_order_info = get_order_info_by_id(order_id)
            context_final = {"info": full_order_info}
            return render(request=request, template_name="order_created.html", context=context_final)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
            cont = {"form": form}
            return render(request=request, template_name="order_create.html", context=cont)
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(["GET", "POST"])
def order_create_from_product_card_controller(request: HttpRequest, item_id: int) -> HttpResponse:
    order_data_items = []
    try:
        item_from_db = get_product_by_id(item_id=int(item_id))
        currencies = get_currencies_names_from_items([item_from_db])
        item_dto = create_order_item_dto_by_item_id(item_id=item_id)
        order_data_items.append(item_dto)
    except ItemNotFoundError:
        return HttpResponseBadRequest("Item with provided ID not found in the database.")
    if request.method == "GET":
        form = SubmitOrderForm(currencies=currencies)
        context = {"item": item_from_db, "form": form}
        return render(request=request, template_name="order_create.html", context=context)

    elif request.method == "POST":
        form = SubmitOrderForm(currencies, request.POST)
        if form.is_valid():
            order_data = convert_data_from_request_to_dto(dto=OrderDTO, data_from_request=form.cleaned_data)
            order_data.items = order_data_items
            order_id = create_order(order_dto=order_data)
            full_order_info = get_order_info_by_id(order_id)
            context_final = {"info": full_order_info}
            return render(request=request, template_name="order_created.html", context=context_final)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
            cont = {"form": form}
            return render(request=request, template_name="order_create.html", context=cont)
    return HttpResponseBadRequest("Incorrect HTTP method.")
