from django.contrib import admin

from .models import Order
from .models import OrderCustomer
from .models import PayPalPlan
from .models import PayPalProduct
from .models import PayPalSubscription
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


@admin.register(PayPalProduct)
class PayPalProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "paypal_id",
    )
    search_fields = (
        "product.name",
        "paypal_id",
    )
    list_filter = ["product"]


@admin.register(PayPalPlan)
class PayPalPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "plan_id",
    )
    search_fields = (
        "product.name",
        "plan_id",
    )
    list_filter = ["product"]


@admin.register(PayPalSubscription)
class PayPalSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subscription_id",
        "plan",
    )
    search_fields = ("plan.plan_id", "subscription_id")
    list_filter = ["plan"]


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
