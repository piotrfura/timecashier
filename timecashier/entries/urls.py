from django.urls import path
from .views import clients_list, entries_list, client_details, whereami, client_nearby

app_name = 'entries'

urlpatterns = [
    path('clients/', clients_list, name='clients'),
    path('entries/', entries_list, name='entries'),
    path('clients/<slug:client_slug>/', client_details, name='client_details'),
    path('whereami/', whereami, name='whereami'),
    # path('ajax/client_nearby/', client_nearby, name='client_nearby'),
]