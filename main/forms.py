from allauth.account.forms import LoginForm
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
                FloatingField("password", placeholder="Enter Password"),
                Field("remember", placeholder="Enter Password"),
                Submit(
                    "submit",
                    "Zaloguj",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px; margin-bottom: 10px;",
                ),
            )
        )
