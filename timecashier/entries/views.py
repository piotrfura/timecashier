from django.shortcuts import render
from main.forms import LocationForm, NewEntryForm
from entries.models import Client, Entry, Location
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.views import index
import datetime

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


def whereami(request):
    nearest_client = Client.objects.last()
    clients_dist = {}
    clients = Client.objects.all()


    if request.user.is_authenticated:
        initial_dict = {
            "client": nearest_client.id,
            "start_date": datetime.datetime.today().date(),
            "start_time": datetime.datetime.now().time(),
            # "duration": datetime.time(0, 0, 0)
        }

        active_entries = Entry.objects.filter(user=request.user, duration__isnull=True)
        form = NewEntryForm(initial=initial_dict)
        # form = NewEntryForm()

        context = {
            "clients_list": clients,
            "nearest_client": nearest_client,
            "form": form,
            "active_entries": active_entries
        }
        return render(request, 'entries/whereami.html', context)

    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_authenticated:

        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        location = Location.objects.create(longitude=longitude, latitude=latitude, user=request.user)
        for client in clients:
            length = abs(
                ((float(client.longitude) - float(longitude)) ** 2 + (float(client.latitude) - float(latitude)) ** 2) ** (0.5))
            clients_dist[client] = length
        min_dist = min(clients_dist.values())
        nearest_client = [client for client in clients_dist if clients_dist[client] == min_dist][0]

    if request.method == "POST" and request.user.is_authenticated:

        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            form.cleaned_data['client'] = Client.objects.get(id=form.cleaned_data['client'])
            entry = Entry.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse("entries:whereami"))


