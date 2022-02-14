from django.shortcuts import render
#from django.http import HttpResponse
from entries.models import Client, Entry
from .forms import NewEntryForm
from . import services
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):


    if request.method == "POST" and request.user.is_authenticated:
        # data = {
        #     "start": request.POST.get('start', None),
        #     "end": request.POST.get('end', None),
        #     "client": Client.objects.get(pk=request.POST['client']),
        #     "user": request.user,
        # }
        # entry = Entry.objects.create(**data)

        form = NewEntryForm(data=request.POST)
        if form.is_valid():
            services.save_entry(form.cleaned_data)
            return HttpResponseRedirect(reverse("index"))
    else:

        clients_dist = {}
        clients = Client.objects.all()

        lat_user = 52.2518528
        long_user = 21.0468864

        for client in clients:
            length = abs(
                ((float(client.longitude) - long_user) ** 2 + (float(client.latitude) - lat_user) ** 2) ** (0.5))
            clients_dist[client] = length
        min_dist = min(clients_dist.values())
        nearest_client = [client for client in clients_dist if clients_dist[client] == min_dist][0]

        active_entries = Entry.objects.filter(end__isnull=True)

        form = NewEntryForm()

    context = {
            "nearest_client": nearest_client,
               "clients_list": clients,
               "active_entries": active_entries,
               "form": form
    }
    return render(request, 'main/index.html', context)

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
