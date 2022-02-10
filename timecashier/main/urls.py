from django.urls import path
from main.views import index, about, test

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('test/', test, name='test'),
]