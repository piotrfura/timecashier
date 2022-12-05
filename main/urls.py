from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import access
from .views import change_password
from .views import index
from entries.views import client_nearby
from entries.views import home

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("entry", home, name="entry"),
    path("ajax/client_nearby/", client_nearby, name="client_nearby"),
    path("accounts/login/", access, name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/password_change/", change_password, name="change_password"),
]
