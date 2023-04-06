from django.contrib.auth.models import User
from django.db import models

from main.models import Organization


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.SmallIntegerField(default=1)
    billing_cycle_unit = models.CharField(max_length=1, default="M")
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
    active = models.BooleanField(default=False)
    last_payment = models.DateTimeField(null=True, blank=True)

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


class PayPalProduct(models.Model):
    paypal_id = models.CharField(max_length=100)
    paypal_name = models.CharField(max_length=255)
    paypal_description = models.TextField(null=True, blank=True)
    paypal_create_time = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="paypal_product"
    )

    def __str__(self):
        return f"{self.product.pk} {self.product.name} {self.paypal_id}"


class PayPalPlan(models.Model):
    plan_id = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="paypal_plan"
    )

    def __str__(self):
        return f"Plan {self.product.pk} {self.product.name} {self.plan_id}"


class PayPalSubscription(models.Model):
    subscription_id = models.CharField(max_length=100)
    plan = models.ForeignKey(
        PayPalPlan, on_delete=models.CASCADE, related_name="paypal_subscription"
    )
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Subscription {self.subscription_id} {self.plan.plan_id} {self.plan.product.name} {self.status}"
