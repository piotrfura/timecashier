from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add_to_order/<int:pk>/", views.order_create, name="add_to_order"),
    path("order/<int:pk>/", views.order_submit, name="order_create"),
]
