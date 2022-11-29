from django.urls import path
from .views import clients_list, entries_list, client_details, entry_details, entry_save, client_edit, client_add

app_name = 'entries'

urlpatterns = [
    path('clients/', clients_list, name='clients'),
    path('entries/', entries_list, name='entries'),
    path('clients/<slug:client_slug>', client_details, name='client_details'),
    path('clients/edit/<int:client_id>', client_edit, name='client_edit'),
    path('clients/edit/add/', client_add, name='client_add'),
    path('entries/<int:entry_id>', entry_details, name='entry_details'),
    path('entries/save/<int:entry_id>', entry_save, name='entry_save'),
]
