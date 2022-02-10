from django.urls import path
from main.views import index, about, test

app_name = 'main'

urlpatterns = [
    path('', index),
    path('about/', about, name='about'),
    path('test/', test, name='test'),
]