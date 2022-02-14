from django import forms
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder


class NewEntryForm(forms.Form):
    client = forms.IntegerField(label="Klient (na podstawie lokalizacji)")
    start = forms.DateTimeField(label="Start", required=False)
    end = forms.DateTimeField(label="Koniec", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_action = 'contact'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'client',
                'start',
                'end'
            ),
            ButtonHolder(
                Submit('submit', 'DODAJ', css_class='btn btn-primary'),
                css_class="d-flex justify-content-end"
            ),
        )

