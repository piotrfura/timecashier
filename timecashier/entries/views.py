from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# from django.views.generic import View
from django.http import JsonResponse

from time import time
from entries.models import Client, Entry
# Create your views here.

def clients_list(request):
    clients = Client.objects.all()
    context = {'clients_list': clients}
    return render(request, "entries/clients.html", context)


def entries_list(request):
    entries = Entry.objects.all().filter(user=request.user).order_by("-created")
    context = {'entries_list': entries}
    return render(request, "entries/entries.html", context)


def client_details(request, client_slug):
    client = Client.objects.filter(active=True).get(slug=client_slug)

    client_link = f'http://maps.google.com/maps?q= {client.latitude},{client.longitude}'
    context = {'client': client, 'client_link': client_link}
    return render(request, "entries/client_details.html", context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def whereami(request):
    longitude = request.GET.get('longitude')
    latitude = request.GET.get('latitude')
    print(longitude, latitude)

    if is_ajax(request):
        t = time()

        return JsonResponse({'seconds': t}, status=200)

    return render(request, "entries/whereami.html")

