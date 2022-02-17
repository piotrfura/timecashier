from django.shortcuts import render, get_object_or_404
from entries.models import Client, Entry, Location
from main.forms import NewEntryForm
# from django.http import HttpResponseRedirect
from datetime import datetime

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

def entry_details(request, entry_id):
    entry_details = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry_details.start.strftime("%Y-%m-%dT%H:%M"),
        "end": datetime.now().strftime("%Y-%m-%dT%H:%M"),#yyyy-MM-ddThh:mm
    }
    form = NewEntryForm(instance=entry_details, initial=initial_dict)
    context = {
        'entry_details': entry_details,
        'form': form}
    return render(request, "entries/entry_details.html", context)