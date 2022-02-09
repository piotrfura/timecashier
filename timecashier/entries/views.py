# from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, Entry


# Create your views here.

def show_clients(request):
    html = """<ul>"""
    for client in Client.objects.all():
        html += f"<li>{client}</li>"
    html += "</ul>"
    return HttpResponse(html)


def show_client1(request):
    client = Client.objects.first()
    html = f"""<h2>{client.name}</h2>"""
    html += f'''<div>
            <small>Utworzono: {client.created}, zmodyfikowano: {client.modified}</small>
        </div>
        <div>
            <p>Nazwa Klienta: {client.name}</p>
        </div>'''
    return HttpResponse(html)


def show_entries(request):
    html = """<ul>"""
    for entry in Entry.objects.all():
        html += f"<li>{entry}</li>"
    html += "</ul>"
    return HttpResponse(html)

