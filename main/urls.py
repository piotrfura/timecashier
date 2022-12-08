from django.urls import path

from .views import index
from entries.views import client_nearby
from entries.views import home

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("entry", home, name="entry"),
    path("ajax/client_nearby/", client_nearby, name="client_nearby"),
]
