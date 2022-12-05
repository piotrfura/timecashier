from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from main.forms import LoginForm
from main.forms import UserProfileForm


def index(request):
    return render(request, "main/index.html")


def access(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("entries:home"))
        if user is None:
            messages.error(request, "Nieprawidłowy użytkownik lub hasło!")
            return HttpResponseRedirect(reverse("main:login"))
    else:
        form = LoginForm()
    return render(request, "main/login.html", {"form": form})


@login_required
def change_password(request):
    username = request.user
    if request.method == "POST":
        form = UserProfileForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Hasło zostało poprawnie zmienione!")
            return HttpResponseRedirect(reverse("entries:home"))
        else:
            messages.error(
                request, "Wprowadzono błędne dane! Popraw i spróbuj ponownie."
            )
    else:
        form = UserProfileForm(request.user)
    return render(
        request,
        "main/change_password.html",
        {
            "form": form,
            "username": username,
        },
    )


def lockout(request, credentials, *args, **kwargs):
    messages.error(
        request,
        "Zbyt wiele prób logowania. Konto zostało zablokowane. Skontaktuj się z administratorem.",
    )
    return HttpResponseRedirect(reverse("main:index"))
