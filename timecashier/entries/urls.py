from django.urls import path
from .views import clients_list, entries_list, client_details, entry_details

app_name = 'entries'

urlpatterns = [
    path('clients/', clients_list, name='clients'),
    path('entries/', entries_list, name='entries'),
    path('clients/<slug:client_slug>/', client_details, name='client_details'),
    path('entries/<int:entry_id>/', entry_details, name='entry_details'),
    path('entries/<int:entry_id>/entry', entry_details, name='entry'),

]