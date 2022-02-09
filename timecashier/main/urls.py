from django.urls import path
from main.views import hello_world, about, test

urlpatterns = [
    path('', hello_world),
    path('about/', about),
    path('test/', test),
]