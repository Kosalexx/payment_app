from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from payment.business_logic.api import (
    create_checkout_session,
    create_payment_intent,
    get_stripe_settings_by_currency_name,
)
from shop.business_logic.services import get_order_info_by_id

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
def buy_using_stripe_session_controller(request: HttpRequest, order_id: int) -> JsonResponse:
    """Stripe PaymentIntent controller."""

    try:
        order_info = get_order_info_by_id(order_id=order_id)

        checkout_session = create_checkout_session(request=request, data=order_info)

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


@require_http_methods(request_method_list=["POST"])
def buy_using_stripe_payment_intent(request: HttpRequest, order_id: int) -> JsonResponse:
    try:
        order_info = get_order_info_by_id(order_id=order_id)

        payment_intent = create_payment_intent(data=order_info)

        return JsonResponse({"clientSecret": payment_intent["client_secret"]})
    except Exception as err:
        logger.error(msg="Raised exception!", exc_info=err)
        return JsonResponse({"error": str(err)})


@require_http_methods(request_method_list=["GET"])
def payment_intent_form_controller(request: HttpRequest, order_id: int) -> HttpRequest:
    order_data = get_order_info_by_id(order_id=order_id)
    context = {"info": order_data}
    return render(request=request, template_name="order_payment_intent.html", context=context)
