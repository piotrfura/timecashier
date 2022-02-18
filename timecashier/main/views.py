from django.shortcuts import render
from entries.models import Client, Entry, Location
from .forms import NewEntryForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import date, datetime
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def index(request):
    initial_dict = {
        "start": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }
    clients = Client.objects.all()
    clients_dist = {}
    active_entries = Entry.objects.filter(user=request.user, end__isnull=True)

    if request.method == "POST" and request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_authenticated:
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        location = Location.objects.create(longitude=longitude, latitude=latitude, user=request.user)

    if request.method == "POST" and request.user.is_authenticated:

        form = NewEntryForm(request.POST)
        if form.is_valid() and len(active_entries) == 0:
            form.cleaned_data['user'] = request.user
            entry = Entry.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse("main:index"))
        else:
            messages.error(request, 'Przed dodaniem kolejnego zadania musisz zakończyć poprzednie!')

    else:
        form = NewEntryForm(initial=initial_dict)

    context = {
        "form": form,
        "active_entries": active_entries
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

def test(request):
    task_list = ['Pranie', 'Sprzątanie', 'Praca', 'Jedzenie']
    tekst = 'Jakiś tekst testowy tutaj dam...'
    languages = {
        'python': 'advanced',
        'sql': 'intermediate',
        'js': 'beginner'
    }
    context = {'tasks': task_list, 'text': tekst, 'languages':languages}
    return render(request, 'main/test.html', context)
