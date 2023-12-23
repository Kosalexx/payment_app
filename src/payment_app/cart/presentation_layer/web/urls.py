from cart.presentation_layer.web.views import (
    cart_add,
    cart_delete,
    cart_update,
    cart_view,
    clear_cart,
)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", cart_view, name="cart-view"),
    path("add/", cart_add, name="add-to-cart"),
    path("delete/", cart_delete, name="delete-to-cart"),
    path("update/", cart_update, name="update-to-cart"),
    path("clear/", clear_cart, name="clear-cart"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
