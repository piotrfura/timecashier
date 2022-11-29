from django.urls import path

from .views import about
from .views import change_password
from .views import client_nearby
from .views import home
from .views import index

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('entry', home, name='entry'),
    path('ajax/client_nearby/', client_nearby, name='client_nearby'),
    path('change_password/', change_password, name='change_password'),
]
