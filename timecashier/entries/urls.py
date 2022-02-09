from django.urls import path
from .views import clients_list, entries_list, client_details

urlpatterns = [
    path('clients/', clients_list),
    path('entries/', entries_list),
    path('clients/<int:client_id>/', client_details)
]