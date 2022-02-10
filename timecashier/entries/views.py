from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Client, Entry


# Create your views here.

def clients_list(request):
    clients = Client.objects.all()
    context = {'clients_list': clients}
    return render(request, "entries/clients.html", context)


def entries_list(request):
    entries = Entry.objects.all()
    context = {'entries_list': entries}
    return render(request, "entries/entries.html", context)


def client_details(request, client_id):
    client = Client.objects.get(pk=client_id)
    client_link = f'http://maps.google.com/maps?q= {client.latitude},{client.longitude}'
    context = {'client': client, 'client_link': client_link}
    return render(request, "entries/client_details.html", context)

def whereami(request):
    return render(request, "entries/whereami.html")