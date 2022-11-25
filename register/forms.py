from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from crispy_bootstrap5.bootstrap5 import FloatingField


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = "breathingForm"
        self.helper.layout = Layout(
            Div(
                Div(
                    FloatingField("username"),
                    FloatingField("email"),
                    FloatingField("password1"),
                    FloatingField("password2"),
                    Submit('submit', 'Rejestruj', css_class='btn-primary rounded-pill w-100',
                               style='margin-top: 30px;'),
                ), css_class='container col col-md-4 justify-content-center panel-background'
            )
        )