from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Order


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == "Completed":
        order = get_object_or_404(Order, pk=ipn.invoice)

        if order.product.price == ipn.mc_gross:
            order.paid = True
            order.save()
