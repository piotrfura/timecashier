from django.shortcuts import render
from entries.models import Client, Entry, Location
from .forms import NewEntryForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import date, datetime
from django.http import JsonResponse
from django.contrib import messages
from datetime import timedelta, time

# Create your views here.
def index(request):
    initial_dict = {
        "start": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }
    clients = Client.objects.all()
    clients_dist = {}
    entries = Entry.objects.filter(user=request.user, inactive=False, end__isnull=False)
    active_entries = Entry.objects.filter(user=request.user, inactive=False, end__isnull=True)

    if request.method == "POST" and request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_authenticated:
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        location = Location.objects.create(longitude=longitude, latitude=latitude, user=request.user)

    if request.method == "POST" and request.user.is_authenticated:

        form = NewEntryForm(request.POST)
        if form.is_valid() and len(active_entries) == 0:
            form.cleaned_data['user'] = request.user
            start_time = form.cleaned_data['start']
            end_time = form.cleaned_data['end']
            if end_time is None:
                entry = Entry.objects.create(**form.cleaned_data)
                messages.success(request, 'Pomyślnie rozpoczęto nowe zadanie!')
            if end_time is not None and end_time >= start_time:
                form.cleaned_data['duration'] = end_time - start_time
                entry = Entry.objects.create(**form.cleaned_data)
                messages.success(request, 'Pomyślnie dodano zadanie!')
            if end_time is not None and end_time < start_time:
                messages.error(request, 'Data zakończenia musi być późniejsza od daty startu!')
            return HttpResponseRedirect(reverse("main:index"))
        if len(active_entries) != 0:
            messages.error(request, 'Przed dodaniem kolejnego zadania musisz zakończyć poprzednie!')

    else:
        form = NewEntryForm(initial=initial_dict)

    context = {
        "form": form,
        "active_entries": active_entries,
        "entries": entries,
    }

    return render(request, 'main/index.html', context)


def client_nearby(request):
    clients = Client.objects.all()
    clients_dist = {}

    longitude = request.GET.get('longitude')
    latitude = request.GET.get('latitude')

    for client in clients:
        length = abs(
            ((float(client.longitude) - float(longitude)) ** 2 + (float(client.latitude) - float(latitude)) ** 2) ** (
                0.5))
        clients_dist[client] = length
    min_dist = min(clients_dist.values())
    nearest_client = [client for client in clients_dist if clients_dist[client] == min_dist][0]
    data = {
        'nearest_client': nearest_client.id
    }
    return JsonResponse(data)

def about(request):
    return render(request, 'main/about.html')