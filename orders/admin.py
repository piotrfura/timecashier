from django.contrib import admin

from .models import Order
from .models import OrderCustomer
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "created",
    )
    search_fields = ("name",)
    list_filter = ("created",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "active",
        "last_payment",
        "product",
        "created",
        "modified",
    )
    list_filter = ("created",)


@admin.register(OrderCustomer)
class OrderCustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "created",
    )
    list_filter = ("created",)
