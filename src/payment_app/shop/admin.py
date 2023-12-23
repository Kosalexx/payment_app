from typing import Any

from django.contrib import admin
from django.utils.safestring import mark_safe
from shop.models import Currency, Discount, Item, Order, OrderItem, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "get_html_photo", "description", "currency", "price", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    ordering = ["created_at"]
    fields = [
        "name",
        "description",
        "currency",
        "price",
        "photo",
        "created_at",
        "get_html_photo",
    ]
    readonly_fields = ["created_at", "updated_at", "get_html_photo"]
    list_per_page = 10

    @admin.decorators.display(description="Item photo")
    def get_html_photo(self, object: Item) -> Any | None:
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        else:
            return None


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_display_links = ["id", "name"]
    ordering = ["id"]
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "paid", "customer_email", "tax", "discount", "created_at", "updated_at"]
    list_display_links = ["id"]
    ordering = ["created_at"]
    fields = [
        "paid",
        "customer_email",
        "tax",
        "discount",
        "created_at",
    ]
    readonly_fields = ["created_at", "updated_at"]

    @admin.decorators.display(description="Item photo")
    def get_html_photo(self, object: Item) -> Any | None:
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        else:
            return None


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "item", "quantity", "created_at"]
    list_display_links = ["id"]
    ordering = ["created_at"]
    list_per_page = 10


class TaxAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "value", "stripe_id"]
    list_display_links = ["id", "name"]
    ordering = ["created_at"]
    list_per_page = 10


class DiscountAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "percent_off", "created_at"]
    list_display_links = ["id", "name"]
    ordering = ["created_at"]
    list_per_page = 10


admin.site.register(Item, ItemAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)
