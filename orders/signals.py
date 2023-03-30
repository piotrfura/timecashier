from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Order


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender

    # check for subscription signup IPN
    if ipn_obj.txn_type == "subscr_signup":
        pass

    elif ipn_obj.txn_type == "subscr_payment":

        order = get_object_or_404(Order, id=ipn_obj.invoice)
        if order.product.price == ipn_obj.mc_gross:
            # get user id and extend the subscription
            id = ipn_obj.custom
            user = User.objects.get(id=id)
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.active = True
            order.last_payment = datetime.now()
            order.save()

            subject = "Potwierdzenie subskrypcji Timecashier {{ order.product.name }}"

            message = (
                "Dziękujemy za opłacenie subskrypcji planu Timecashier "
                + {{order.product.name}}
                + " !/nTwój dostęp jest już aktywny./nZapraszamy do korzystania z portalu TimeCashier.pl"
            )

            email = EmailMessage(
                subject,
                message,
                "TimeCashier.pl <noreply@timecashier.pl>",
                [user.email],
            )

            email.send()

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        pass

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        pass
