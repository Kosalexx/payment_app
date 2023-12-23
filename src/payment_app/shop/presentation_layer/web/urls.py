from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from shop.presentation_layer.web import views

urlpatterns = [
    path("", views.index_controller, name="index"),
    path("item/add", views.add_item_controller, name="add-item"),
    path("item/<int:item_id>", views.item_info_controller, name="item-info"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
