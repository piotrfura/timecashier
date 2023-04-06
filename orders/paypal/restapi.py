from datetime import datetime
from datetime import timedelta

import paypalrestsdk
import pytz
from django.conf import settings

from orders.models import PayPalPlan
from orders.models import PayPalProduct
from orders.models import Product


paypal_api = paypalrestsdk.Api(
    {
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    }
)


def create_product(product):

    data = {
        "name": product.name,
        "description": product.description,
    }
    response = paypal_api.post("/v1/catalogs/products", data)
    return response


def create_all_paypal_products():
    products = Product.objects.filter(active=True)
    for product in products:
        try:
            PayPalProduct.objects.get(product=product)
        except PayPalProduct.DoesNotExist:
            paypal_response = create_product(product)
            paypal_product = PayPalProduct(
                product=product,
                paypal_id=paypal_response["id"],
                paypal_name=paypal_response["name"],
                paypal_description=paypal_response["description"],
                paypal_create_time=paypal_response["create_time"],
            )
            paypal_product.save()
    return True


def create_plan(product):

    create_all_paypal_products()
    paypal_product = PayPalProduct.objects.get(product=product)

    data = {
        "product_id": paypal_product.paypal_id,
        "name": product.name,
        "description": product.description,
        "status": "ACTIVE",
        "billing_cycles": [
            {
                "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": f"{product.price:.2f}",
                        "currency_code": "PLN",
                    }
                },
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": "true",
            "setup_fee": {"value": "0", "currency_code": "PLN"},
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3,
        },
    }
    try:
        plan_id = PayPalPlan.objects.get(product=product).plan_id
        return plan_id
    except PayPalPlan.DoesNotExist:
        response = paypal_api.post("v1/billing/plans", data)
        plan_id = response["id"]
        paypal_plan = PayPalPlan(product=product, plan_id=plan_id)
        paypal_plan.save()
    return plan_id


def create_subscription(**kwargs):

    data = {
        "plan_id": 1,
        "start_time": (
            datetime.now(pytz.timezone("Europe/Warsaw")) + timedelta(minutes=1)
        ).isoformat(),
        "subscriber": {
            "name": {"given_name": "John", "surname": "Smith"},
            "email_address": "john.smith@example.com",
        },
        "application_context": {
            "brand_name": "TimeCashier.pl",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED",
            },
            "return_url": "https://timecashier.pl/",
            "cancel_url": "https://timecashier.pl/",
        },
    }

    data.update(kwargs)
    response = paypal_api.post("/v1/billing/subscriptions", data)
    return response


def cancel_subscription(subscription_id):
    paypal_api.post(f"/v1/billing/subscriptions/{subscription_id}/cancel")
    return True


def list_plan():
    response = paypal_api.get("/v1/billing/plans")
    return response


def list_product():
    response = paypal_api.get("/v1/catalogs/products")
    return response
