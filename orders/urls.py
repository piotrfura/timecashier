from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add_to_order/<int:pk>/", views.order_create, name="add_to_order"),
    path("order/<int:pk>/", views.order_submit, name="order_create"),
    path("process_payment/", views.process_payment, name="process_payment"),
    path("payment-done/", views.payment_done, name="payment_done"),
    path("payment-cancelled/", views.payment_canceled, name="payment_cancelled"),
    path("paypal-hook/", views.paypal_hook, name="paypal-hook"),
]
