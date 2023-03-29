from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from .models import Order


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender

    # check for Buy Now IPN
    if ipn_obj.txn_type == "web_accept":

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            print("great!")
            order = get_object_or_404(Order, id=ipn_obj.invoice)

            if order.get_total_cost() == ipn_obj.mc_gross:
                # mark the order as paid
                order.paid = True
                order.save()

    # check for subscription signup IPN
    elif ipn_obj.txn_type == "subscr_signup":

        # get user id and activate the account
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        user.active = True
        user.save()

        subject = "Sign Up Complete"

        message = "Thanks for signing up!"

        email = EmailMessage(subject, message, "noreply@timecashier.pl", [user.email])

        email.send()
    elif ipn_obj.txn_type == "subscr_payment":

        # get user id and extend the subscription
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        # user.extend()  # extend the subscription
        order = Order.objects.get(pk=ipn_obj.invoice)
        order.active = True
        order.last_payment = datetime.now()
        order.save()

        subject = "Your Invoice for {} is available".format(
            datetime.strftime(datetime.now(), "%b %Y")
        )

        message = (
            "Thanks for using our service. The balance was automatically "
            "charged to your credit card."
        )

        email = EmailMessage(subject, message, "noreply@timecashier.pl", [user.email])

        email.send()

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        pass

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        pass
