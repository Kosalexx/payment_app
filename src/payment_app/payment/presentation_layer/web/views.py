from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from payment.business_logic.api import (
    create_checkout_session,
    get_stripe_settings_by_currency_name,
)
from shop.business_logic.services import get_product_by_id

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(
    request_method_list=[
        "GET",
    ]
)
def get_stripe_config(request: HttpRequest, slug: str) -> JsonResponse:
    """Return public key depends on items' currency."""
    if request.method == "GET":
        conf = get_stripe_settings_by_currency_name(cur_name=slug)
        stripe_config = {"publicKey": conf["publishableKey"]}
        return JsonResponse(stripe_config, safe=False)


@require_http_methods(request_method_list=["GET"])
def buy_using_stripe_session_controller(request: HttpRequest, item_id: int) -> JsonResponse:
    """Index page controller."""

    try:
        product_info = get_product_by_id(item_id=item_id)

        checkout_session = create_checkout_session(request=request, data=product_info)

        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as err:
        logger.error(msg="Raised exception!", exc_info=err)
        return JsonResponse({"error": str(err)})


def payment_success(request: HttpRequest) -> HttpResponse:
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]
    return render(request, "success.html")


def payment_failed(request: HttpRequest) -> HttpResponse:
    return render(request, "failed.html")
