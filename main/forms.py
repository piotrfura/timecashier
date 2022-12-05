from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            Div(
                FloatingField("username"),
                FloatingField("password"),
                Submit(
                    "login",
                    "Zaloguj",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px;",
                ),
                css_class="container col col-md-5 justify-content-center panel-background shadow p-3",
            )
        )


class UserProfileForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            Div(
                FloatingField("old_password"),
                FloatingField("new_password1"),
                FloatingField("new_password2"),
                Submit(
                    "submit",
                    "Zmień hasło",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
                css_class="container col col-md-6 justify-content-center panel-background shadow",
            )
        )
