import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from paypalrestsdk.notifications import WebhookEvent

from .forms import OrderCreateForm
from .models import Order
from .models import PayPalPlan
from .models import PayPalSubscription
from .models import Product
from entries.views import get_user_org
from orders.paypal.restapi import create_subscription

logger = logging.getLogger(__name__)


def product_list(request):
    products = Product.objects.all().order_by("price")
    return render(request, "orders/product_list.html", {"products": products})


@require_POST
def order_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order = Order.objects.create(
        user=request.user, organization=get_user_org(request), product=product
    )
    return redirect("orders:order_create", order.pk)


def order_submit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user = request.user
    if request.method == "POST":
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order_customer = order_form.save(commit=False)
            order_customer.user = user
            order_customer.order = order
            order_customer.save()
            request.session["order_id"] = order.pk

            plan = PayPalPlan.objects.get(product=order.product)

            paypal_dict = {
                "plan_id": plan.plan_id,
                "subscriber": {
                    "name": {"given_name": order_customer.name, "surname": ""},
                    "email_address": order_customer.email,
                },
                "application_context": {
                    "brand_name": "TimeCashier.pl",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                        "payer_selected": "PAYPAL",
                        "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED",
                    },
                    "return_url": request.build_absolute_uri(
                        reverse("orders:payment_done")
                    ),
                    "cancel_url": request.build_absolute_uri(
                        reverse("orders:payment_cancelled")
                    ),
                },
            }

            api_response = create_subscription(**paypal_dict)
            approve_url = api_response["links"][0]["href"]
            request.session["approve_url"] = approve_url
            sub = PayPalSubscription(
                subscription_id=api_response["id"],
                plan=plan,
                status=api_response["status"],
            )
            sub.save()
            return HttpResponseRedirect(reverse("orders:process_payment"))
    else:
        order_form = OrderCreateForm(
            initial={
                "order": order.pk,
                "name": user.get_full_name(),
                "email": user.email,
            }
        )
    return render(
        request,
        "orders/order_submit.html",
        {"order": order, "order_form": order_form, "user": user},
    )


@csrf_exempt
def payment_done(request):
    messages.success(
        request,
        "Dziękujemy za złożenie zamówienia! "
        + "Po potwierdzeniu płatności Twój dostęp zostanie aktywowany. "
        + "Potwierdzenie otrzymasz na adres mailowy w ciągu kilku minut.",
    )
    return HttpResponseRedirect(reverse("main:profile"))


@csrf_exempt
def payment_canceled(request):
    messages.error(request, "Płatność została anulowana. Spróbuj ponownie.")
    return HttpResponseRedirect(reverse("orders:process_payment"))


@login_required
def process_payment(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, pk=order_id)

    approve_url = request.session.get("approve_url")

    context = {"order": order, "approve_url": approve_url}
    return render(request, "orders/process_payment.html", context)


@csrf_exempt
def paypal_hook(request):
    transmission_id = request.headers["Paypal-Transmission-Id"]
    timestamp = request.headers["Paypal-Transmission-Time"]
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    event_body = request.body.decode("utf-8")
    cert_url = request.headers["Paypal-Cert-Url"]
    auth_algo = request.headers["Paypal-Auth-Algo"]
    actual_signature = request.headers["Paypal-Transmission-Sig"]
    response = WebhookEvent.verify(
        transmission_id,
        timestamp,
        webhook_id,
        event_body,
        cert_url,
        actual_signature,
        auth_algo,
    )
    if response:
        obj = json.loads(request.body)
        event_type = obj.get("event_type")
        resource = obj.get("resource")
        logger.info(event_type, resource)
        if event_type == "PAYMENT.SALE.COMPLETED":
            sub = PayPalSubscription.objects.get(
                subscription_id=resource["billing_agreement_id"]
            )
            sub.status = resource["state"]
            sub.save()
            logger.info(f"subscription {resource['billing_agreement_id']} paid")
    return HttpResponse(status=200)
