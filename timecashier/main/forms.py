from django import forms
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Column
from entries.models import Entry, Client
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


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
        self.helper.form_action = ''
        self.fields['start'].label = 'Start'
        self.fields['start'].widget = forms.DateInput(attrs={'required': True, 'type': 'datetime-local'})
        self.fields['end'].label = 'Koniec'
        self.fields['end'].widget = forms.DateInput(attrs={'required': False, 'type': 'datetime-local'})
        self.fields['client'].label = 'Klient'

        self.helper.layout = Layout(
            Div(
                Div(
                    Column('client', css_class='col-md'),
                    Column('start', css_class='col-md'),
                    Column('end', css_class='col-md'),
                    Submit('submit', 'DODAJ', css_class='col-md rounded-pill m-4'),
                    css_class='row'
                ),
                css_class='container'
            )
        )


class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['start', 'end', 'client', 'description', 'inactive']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.fields['start'].label = 'Start'
        self.fields['start'].widget = forms.DateInput(attrs={'required': True, 'type': 'datetime-local'})
        self.fields['end'].label = 'Koniec'
        self.fields['end'].widget = forms.DateInput(attrs={'required': False, 'type': 'datetime-local'})
        self.fields['client'].label = 'Klient'
        self.fields['description'].label = 'Opis'
        self.fields['description'].widget = forms.Textarea()
        self.fields['inactive'].label = 'Usuń'

        self.helper.layout = Layout(
            Div(
                Div(
                    'start',
                    'end',
                    'client',
                    'description',
                    'inactive',
                    Submit('submit', 'ZAPISZ', css_class='col-sm btn-danger')
                ),
                css_class='container'
            )
        )



class EditClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'latitude', 'longitude', 'inactive']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.fields['name'].label = 'Nazwa'
        self.fields['latitude'].label = 'Szerokość geograficzna'
        self.fields['latitude'].widget = forms.NumberInput(attrs={'step': 0.0000001, 'max': 90.0000000, 'min': -90.0000000})
        self.fields['longitude'].label = 'Długość geograficzna'
        self.fields['longitude'].widget = forms.NumberInput(attrs={'step': 0.0000001, 'max': 180.0000000, 'min': -180.0000000})
        self.fields['inactive'].label = 'Usuń'

        self.helper.layout = Layout(
            Div(
                Div(
                    'name',
                    'latitude',
                    'longitude',
                    'inactive',
                    Submit('submit', 'ZAPISZ', css_class='col-sm btn-danger')
                ),
                css_class='container'
            )
        )


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        # self.helper.add_input(Submit('login', 'Zaloguj', css_class='btn-primary'))
        self.helper.layout = Layout(
            Div(
                "username",
                "password",
                Submit('login', 'Zaloguj', css_class='btn-primary'),
                css_class='class="col col-sm-4'
            )
        )