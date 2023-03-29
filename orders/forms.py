from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms

from .models import OrderCustomer


# class OrderCreateForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['user']


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderCustomer
        fields = ["business", "tax_no", "name", "email", "address", "city", "zip_code"]
        widgets = {
            "business": forms.CheckboxInput(attrs={"class": "form-control"}),
            "tax_no": forms.TextInput(attrs={"class": "form-control", "hidden": True}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.fields["business"].label = "Kupuję jako firma?"
        # self.fields["business"].widget = forms.ChoiceField(
        #     attrs={
        #         "class": "form-control",
        #     }
        # )
        self.fields["tax_no"].label = "NIP"
        self.fields["name"].label = "Nazwa"
        self.fields["address"].label = "Adres"
        self.fields["zip_code"].label = "Kod pocztowy"
        self.fields["zip_code"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "pattern": "[0-9]{2}-[0-9]{3}",
            }
        )
        self.fields["city"].label = "Miasto"
        self.fields["email"].label = "Email"
        self.helper.layout = Layout(
            Div(
                Div(
                    "business",
                    FloatingField("tax_no"),
                    FloatingField("name"),
                    FloatingField("address"),
                    FloatingField("zip_code"),
                    FloatingField("city"),
                    FloatingField("email"),
                    Submit(
                        "submit",
                        "Zamawiam",
                        css_class="btn-time-primary rounded-pill w-100",
                        style="margin-bottom:10px",
                    ),
                ),
                css_class="container col col-md-6 justify-content-center panel-background shadow",
            )
        )
