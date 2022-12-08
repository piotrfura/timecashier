from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return render(request, "main/index.html")


def lockout(request, credentials, *args, **kwargs):
    messages.error(
        request,
        "Zbyt wiele prób logowania. Konto zostało zablokowane. Skontaktuj się z administratorem.",
    )
    return HttpResponseRedirect(reverse("main:index"))
