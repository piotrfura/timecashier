from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import CustomPayPalPaymentsForm
from .forms import OrderCreateForm
from .models import Order
from .models import Product
from entries.views import get_user_org


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


def process_payment(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, pk=order_id)

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": f"{order.product.price:.2f}",
        "currency_code": "PLN",
        "item_name": "TimeCashier " + order.product.name,
        "invoice": str(order.pk),
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return": request.build_absolute_uri(reverse("orders:payment_done")),
        "cancel_return": request.build_absolute_uri(
            reverse("orders:payment_cancelled")
        ),
        "custom": get_user_org(request).pk,
    }

    payment_form = CustomPayPalPaymentsForm(initial=paypal_dict)
    context = {"order": order, "payment_form": payment_form}
    return render(request, "orders/process_payment.html", context)


@csrf_exempt
def payment_done(request):
    messages.success(request, "Zamówienie zostało opłacone. Dziękujemy za zakup!")
    return HttpResponseRedirect(reverse("main:profile"))


@csrf_exempt
def payment_canceled(request):
    messages.error(request, "Płatność została anulowana. Spróbuj ponownie.")
    return HttpResponseRedirect(reverse("orders:process_payment"))
