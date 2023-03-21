from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column
from crispy_forms.layout import Div
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django import forms

from entries.models import Client
from entries.models import Entry


class LocationForm(forms.Form):

    latitude = forms.CharField()
    longitude = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["start", "end", "client"]

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.fields["start"].label = "Start"
        self.fields["start"].widget = forms.DateInput(
            attrs={"required": True, "type": "datetime-local"}
        )
        self.fields["end"].label = "Koniec"
        self.fields["end"].widget = forms.DateInput(
            attrs={"required": False, "type": "datetime-local"}
        )
        self.fields["client"].label = "Klient"
        self.fields["client"].widget = forms.Select(
            choices=Client.objects.filter(
                inactive=False, organization=self.organization
            ).values_list("id", "name")
        )

        self.helper.layout = Layout(
            Div(
                Column(FloatingField("client", css_class="col-md")),
                Column(FloatingField("start", css_class="col-md")),
                Column(FloatingField("end", css_class="col-md")),
                Submit(
                    "submit",
                    "DODAJ",
                    css_class="btn-time-primary rounded-pill w-100",
                    style="margin-bottom:10px",
                ),
                css_class="row container col justify-content-center panel-background shadow-sm mb-4 mt-2",
            )
        )


class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["start", "end", "client", "description", "inactive"]

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.fields["start"].label = "Start"
        self.fields["start"].widget = forms.DateInput(
            attrs={"required": True, "type": "datetime-local"}
        )
        self.fields["end"].label = "Koniec"
        self.fields["end"].widget = forms.DateInput(
            attrs={"required": False, "type": "datetime-local"}
        )
        self.fields["client"].label = "Klient"
        self.fields["client"].widget = forms.Select(
            choices=Client.objects.filter(
                inactive=False, organization=self.organization
            ).values_list("id", "name")
        )
        self.fields["description"].label = "Opis"
        self.fields["description"].widget = forms.Textarea(attrs={"rows": 5})
        self.fields["inactive"].label = "Usuń"

        self.helper.layout = Layout(
            Div(
                Div(
                    Submit(
                        "submit",
                        "ZAPISZ",
                        css_class="btn-time-primary rounded-pill w-100",
                        style="margin-bottom:20px",
                    ),
                    FloatingField("start"),
                    FloatingField("end"),
                    FloatingField("client"),
                    FloatingField("description", css_class="h-100"),
                    "inactive",
                ),
                css_class="container col col-md-6 justify-content-center panel-background shadow",
            )
        )


class EditClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "latitude", "longitude", "inactive", "logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.fields["name"].label = "Nazwa"
        self.fields["latitude"].label = "Szerokość geograficzna"
        self.fields["latitude"].widget = forms.NumberInput(
            attrs={"step": 0.0000001, "max": 90.0000000, "min": -90.0000000}
        )
        self.fields["longitude"].label = "Długość geograficzna"
        self.fields["longitude"].widget = forms.NumberInput(
            attrs={"step": 0.0000001, "max": 180.0000000, "min": -180.0000000}
        )
        self.fields["inactive"].label = "Usuń"

        self.helper.layout = Layout(
            Div(
                Div(
                    Submit(
                        "submit",
                        "ZAPISZ",
                        css_class="btn-time-primary rounded-pill w-100",
                        style="margin-bottom:10px",
                    ),
                    FloatingField("name"),
                    FloatingField("latitude"),
                    FloatingField("longitude"),
                    "logo",
                    "inactive",
                ),
                css_class="container col col-md-6 justify-content-center panel-background shadow",
            )
        )


class SearchEntriesForm(forms.Form):

    client = forms.ModelChoiceField(
        queryset=Client.objects.filter(inactive=False).values_list("id", "name")
    )
    from_time = forms.DateTimeField()
    to_time = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["from_time"].label = "Od"
        self.fields["to_time"].label = "Do"
        self.fields["client"].label = "Klient"
        self.fields["from_time"].required = False
        self.fields["to_time"].required = False
        self.fields["client"].required = False
        self.fields["from_time"].widget = forms.DateInput(
            attrs={"type": "datetime-local"}
        )
        self.fields["to_time"].widget = forms.DateInput(
            attrs={"type": "datetime-local"}
        )
        self.fields["client"].widget = forms.Select(
            choices=(("", ""),)
            + tuple(
                Client.objects.filter(
                    inactive=False, organization=self.organization
                ).values_list("id", "name")
            )
        )
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            Div(
                Column(FloatingField("client")),
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
