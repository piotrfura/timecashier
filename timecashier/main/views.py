from django.shortcuts import render
#from django.http import HttpResponse
from entries.models import Client, Entry


# Create your views here.
def index(request):
    clients_dist = {}
    clients = Client.objects.all()

    lat_user = 52.2518528
    long_user = 21.0468864

    for client in clients:
        length = abs(((float(client.longitude) - long_user) ** 2 + (float(client.latitude) - lat_user) ** 2) ** (0.5))
        clients_dist[client] = length
    min_dist = min(clients_dist.values())
    nearest_client = [client for client in clients_dist if clients_dist[client] == min_dist][0]
    context = {"nearest_client": nearest_client}
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
