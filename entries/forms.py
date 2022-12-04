from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column
from crispy_forms.layout import Div
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms


class SearchEntriesForm(forms.Form):

    from_time = forms.DateTimeField()
    to_time = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["from_time"].label = "Od"
        self.fields["to_time"].label = "Do"
        self.fields["from_time"].required = False
        self.fields["to_time"].required = False
        self.fields["from_time"].widget = forms.DateInput(
            attrs={"type": "datetime-local"}
        )
        self.fields["to_time"].widget = forms.DateInput(
            attrs={"type": "datetime-local"}
        )
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            Div(
                Column(FloatingField("from_time")),
                Column(FloatingField("to_time")),
                Submit(
                    "submit",
                    "Szukaj",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-top: 10px;",
                ),
                css_class="row container col justify-content-center panel-background shadow-sm my-4",
            )
        )
