from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from payment.presentation_layer.web import views

urlpatterns = [
    path("<int:order_id>/", views.buy_using_stripe_session_controller, name="stripe-session-buy"),
    path("payment_intent/<int:order_id>/", views.buy_using_stripe_payment_intent, name="stripe-payment-intent"),
    path("payment_intent/<int:order_id>/form", views.payment_intent_form_controller, name="payment-intent-form"),
    path("success/", views.payment_success, name="success"),
    path("failed/", views.payment_failed, name="failed"),
    path("config/<slug:slug>/", views.get_stripe_config, name="config"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
