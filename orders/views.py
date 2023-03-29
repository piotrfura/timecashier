from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import OrderCreateForm
from .models import Order
from .models import OrderCustomer
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
            order_customer = OrderCustomer()
            order_customer = order_form.save(commit=False)
            order_customer.user = user
            order_customer.order = order
            order_customer.save()
            messages.success(request, "Pomyślnie złożono zamówienie!")
            return HttpResponseRedirect(reverse("main:profile"))
        else:
            print(order_form.cleaned_data)
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
