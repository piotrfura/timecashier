from django.urls import path

from entries.views import client_nearby
from entries.views import home
from main.views import index
from main.views import PasswordChangeView
from main.views import profile

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("entry", home, name="entry"),
    path("ajax/client_nearby/", client_nearby, name="client_nearby"),
    path("profile/", profile, name="profile"),
    path(
        "accounts/password/change/",
        PasswordChangeView.as_view(),
        name="account_change_password",
    ),
]
