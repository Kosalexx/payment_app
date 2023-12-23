from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from shop.business_logic.services import get_all_products

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(request_method_list=["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    """Index page controller."""

    products = get_all_products()
    context = {"products": products}

    return render(request, "index.html", context=context)
