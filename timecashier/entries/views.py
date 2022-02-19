from django.shortcuts import render, get_object_or_404, redirect
from entries.models import Client, Entry, Location
from main.forms import NewEntryForm, EditEntryForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import DurationField, ExpressionWrapper, F

# Create your views here.

@login_required
def clients_list(request):
    clients = Client.objects.all()
    context = {'clients_list': clients}
    return render(request, "entries/clients.html", context)

@login_required
def entries_list(request):
    entries = Entry.objects.all().filter(user=request.user, inactive=False, end__isnull=False).order_by("-created")
    # Entry.objects.annotate(duration=(ExpressionWrapper((F('end') - F('start')), output_field=DurationField())))
    context = {'entries_list': entries}
    return render(request, "entries/entries.html", context)

@login_required
def client_details(request, client_slug):
    client = Client.objects.filter(inactive=False).get(slug=client_slug)

    client_link = f'http://maps.google.com/maps?q= {client.latitude},{client.longitude}'
    context = {'client': client, 'client_link': client_link}
    return render(request, "entries/client_details.html", context)

@login_required
def entry_save(request, entry_id):
    entry_details = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry_details.start.strftime("%Y-%m-%dT%H:%M"),
        "end": datetime.now().strftime("%Y-%m-%dT%H:%M"),#yyyy-MM-ddThh:mm
    }

    if request.method == "POST" and request.user.is_authenticated:
        form = EditEntryForm(request.POST, instance=entry_details, initial=initial_dict)
        if form.is_valid():
            entry_details = form.save(commit=False)
            entry_details.duration = form.cleaned_data['end'] - form.cleaned_data['start']
            entry_details.save()
            messages.success(request, 'Pomyślnie zapisano zmiany!')
            return HttpResponseRedirect(reverse("main:home"))
        else:
            messages.warning(request, 'Błąd!')

    else:
        form = EditEntryForm(instance=entry_details, initial=initial_dict)

    context = {
        'entry_details': entry_details,
        'form': form}
    return render(request, "entries/entry_details.html", context)

@login_required
def entry_details(request, entry_id):
    entry_details = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry_details.start.strftime("%Y-%m-%dT%H:%M"),
        "end": entry_details.end.strftime("%Y-%m-%dT%H:%M"),#yyyy-MM-ddThh:mm
    }

    if request.method == "POST" and request.user.is_authenticated:
        active_entries = Entry.objects.filter(user=request.user, inactive=False, end__isnull=True)
        form = EditEntryForm(request.POST, instance=entry_details, initial=initial_dict)
        if form.is_valid() and len(active_entries) == 0:
            start_time = form.cleaned_data['start']
            end_time = form.cleaned_data['end']
            if end_time is None:
                entry_details = form.save(commit=False)
                entry_details.duration = None
                entry_details.save()
                messages.success(request, 'Pomyślnie przywrócono zadanie!')
            if end_time is not None and end_time >= start_time:
                entry_details = form.save(commit=False)
                entry_details.duration = end_time - start_time
                entry_details.save()
                messages.success(request, 'Pomyślnie zapisano zadanie!')
            if end_time is not None and end_time < start_time:
                messages.error(request, 'Data zakończenia musi być późniejsza od daty startu!')
            return HttpResponseRedirect(reverse("entries:entries"))
        if form.is_valid() and len(active_entries) != 0:
            messages.error(request, 'Nie można przywrócić zadania. Najpierw zakończ bieżące!')
        else:
            messages.warning(request, 'Błąd formularza!')
    else:
        form = EditEntryForm(instance=entry_details, initial=initial_dict)

    context = {
        'entry_details': entry_details,
        'form': form}
    return render(request, "entries/entry_details.html", context)