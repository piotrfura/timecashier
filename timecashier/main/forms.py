from django import forms
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Column
from entries.models import Entry
from datetime import datetime


class LocationForm(forms.Form):

    latitude = forms.CharField()
    longitude = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['start', 'end', 'client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'entry'
        self.fields['start'].label = 'Start'
        self.fields['start'].widget = forms.DateInput(attrs={'required': True, 'type': 'datetime-local'})
        self.fields['end'].label = 'Koniec'
        self.fields['end'].widget = forms.DateInput(attrs={'required': False, 'type': 'datetime-local'})
        # self.fields['start_time'].widget = forms.TimeInput(attrs={'required': True, 'type': 'time'})
        self.fields['client'].label = 'Klient'

        self.helper.layout = Layout(
            Div(
                Div(
                    Column('start', css_class='col-sm'),
                    Column('end', css_class='col-sm'),
                    Column('client', css_class='col-sm'),
                    Submit('submit', 'DODAJ', css_class='col-sm'),
                    css_class='row'
                ),
                css_class='container'
            )
        )
