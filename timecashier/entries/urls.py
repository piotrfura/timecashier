from django.urls import path
from .views import show_clients, show_entries, show_client1

urlpatterns = [
    path('clients/', show_clients),
    path('entries/', show_entries),
    path('clients/1/', show_client1)

]