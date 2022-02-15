from django import forms
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Div, Column, Row, Field
from entries.models import Client
import datetime

# class DateInput(forms.DateInput):
#     input_type = 'datetime-local'

class NewEntryForm(forms.Form):
    clients = Client.objects.all()
    clients_names = [(client.id, client.name) for client in clients]
    client = forms.CharField(label="Klient (na podstawie lokalizacji)", widget=forms.Select(choices=clients_names))
    start_date = forms.DateField(label="Data", required=False, input_formats=["%d.%m.%Y", ])#, widget=forms.TextInput(attrs={'type':'date', 'placeholder':'dd-mm-yyyy'}), initial=datetime.date.today)
    start_time = forms.TimeField(label="Godzina", required=False, input_formats=["%H:%M:%S"])#, widget=forms.TextInput(attrs={'type':'time'}))
    duration = forms.TimeField(label="Czas", required=False, input_formats=["%H:%M:%S"])#, widget=forms.TextInput(attrs={'type':'time'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row row-cols-lg-auto g-3'
        # self.helper.form_action = 'contact'
        # self.helper.form_class = 'form-vertical'
        # self.helper.field_class = 'col-md-10 col-xs-9'
        self.helper.layout = Layout(
                    'client',
                    'start_date',
                    'start_time',
                    'duration',
                    Submit('submit', 'DODAJ', css_class='btn btn-primary g-4')
            )


class LocationForm(forms.Form):

    latitude = forms.CharField()
    longitude = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
