from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from payment.presentation_layer.web import views

urlpatterns = [
    path("<int:order_id>/", views.buy_using_stripe_session_controller, name="stripe-session-buy"),
    path("success/", views.payment_success, name="success"),
    path("failed/", views.payment_failed, name="failed"),
    path("config/<slug:slug>/", views.get_stripe_config, name="config"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
