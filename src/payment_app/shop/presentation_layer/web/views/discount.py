from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from shop.business_logic.services import get_discounts_list

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(request_method_list=["GET"])
def discounts_table_controller(request: HttpRequest) -> HttpResponse:
    """Discount table controller."""
    if request.method == "GET":
        discounts_data = get_discounts_list()
        context = {"discounts": discounts_data}
        return render(request=request, template_name="discounts.html", context=context)
    return HttpResponseBadRequest("Incorrect HTTP method.")
