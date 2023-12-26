from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from shop.business_logic.dto import AddItemDTO
from shop.business_logic.errors import ItemAlreadyExistsError, ItemNotFoundError
from shop.business_logic.services import (
    create_product,
    get_categories_func,
    get_currencies_func,
    get_product_by_id,
)
from shop.presentation_layer.common.converters import convert_data_from_request_to_dto
from shop.presentation_layer.web.forms import AddItemForm

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
def add_item_controller(request: HttpRequest) -> HttpResponse:
    """Add item controller."""
    currencies = get_currencies_func()
    categories = get_categories_func()
    if request.method == "GET":
        form = AddItemForm(currencies=currencies, categories=categories)
        context = {"form": form}
        return render(request=request, template_name="add_product.html", context=context)
    if request.method == "POST":
        form = AddItemForm(currencies, categories, request.POST, request.FILES)
        if form.is_valid():
            data = convert_data_from_request_to_dto(dto=AddItemDTO, data_from_request=form.cleaned_data)
            try:
                product_id = create_product(data=data)
                logger.info("Product successfully added!", extra={"product_id": product_id})
                return redirect(to="index")
            except ItemAlreadyExistsError:
                context_2 = {
                    "form": form,
                    "err_message": "The item with the entered name already exists... Please try again.",
                }
                return render(request=request, template_name="add_product.html", context=context_2)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
            context_inv = {"form": form}
            return render(request=request, template_name="add_product.html", context=context_inv)
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(
    [
        "GET",
    ]
)
def item_info_controller(request: HttpRequest, item_id: int) -> HttpResponse:
    """Detail item info controller."""

    if request.method == "GET":
        try:
            data = get_product_by_id(item_id=item_id)
            context = {"item": data}
            logger.info(
                "Еhe object has been successfully received.",
                extra={"item_id": data.pk, "item_name": data.name, "item_price": data.price},
            )
            return render(request=request, template_name="item.html", context=context)
        except ItemNotFoundError:
            return HttpResponseBadRequest("Item is not found.")
    return HttpResponseBadRequest("Incorrect HTTP method.")
