from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import LoginForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm
from allauth.account.forms import SetPasswordForm
from allauth.account.forms import SignupForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("login"),
                FloatingField("password"),
                # Field("remember"),
                Submit(
                    "submit",
                    "Zaloguj",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )


class ChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("oldpassword"),
                FloatingField("password1"),
                FloatingField("password2"),
                Submit(
                    "submit",
                    "Zmień hasło",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )


class SignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("email"),
                FloatingField("username"),
                FloatingField("password1"),
                FloatingField("password2"),
                Submit(
                    "submit",
                    "Zarejestruj",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )


class ResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("email"),
                Submit(
                    "submit",
                    "Zresetuj moje hasło",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )


class ResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("password1"),
                FloatingField("password2"),
                Submit(
                    "submit",
                    "Zmień hasło",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )


class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("password1"),
                FloatingField("password2"),
                Submit(
                    "submit",
                    "Ustaw hasło",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )
