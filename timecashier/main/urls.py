from django.urls import path, include
from .views import index, about, client_nearby

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('entry', index, name='entry'),
    path('ajax/client_nearby/', client_nearby, name='client_nearby'),
]