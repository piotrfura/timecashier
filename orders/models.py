from django.contrib.auth.models import User
from django.db import models

from main.models import Organization


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"


class OrderCustomer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="customers")
    business = models.BooleanField(default=False)
    tax_no = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Customer {self.id}"
