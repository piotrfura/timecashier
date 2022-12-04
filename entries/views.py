import json
from datetime import datetime
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from entries.forms import SearchEntriesForm
from entries.models import Client
from entries.models import Entry
from main.forms import EditClientForm
from main.forms import EditEntryForm


@login_required
def clients_list(request):
    clients = Client.objects.filter(inactive=False)
    context = {"clients_list": clients}
    return render(request, "entries/clients.html", context)


@login_required
def entries_list(request):
    initial_dict = {
        "from_time": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M"),
        "to_time": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }
    if request.method == "POST":
        search_session_form = SearchEntriesForm(request.POST)
        if search_session_form.is_valid():
            from_time = search_session_form.cleaned_data["from_time"]
            to_time = search_session_form.cleaned_data["to_time"]
            if from_time and to_time:
                entries = (
                    Entry.objects.all()
                    .filter(
                        start__range=(from_time, to_time),
                        user=request.user,
                        inactive=False,
                        end__isnull=False,
                    )
                    .order_by("-end")
                    .all()
                )
                initial_dict = {
                    "from_time": from_time.strftime("%Y-%m-%dT%H:%M"),
                    "to_time": to_time.strftime("%Y-%m-%dT%H:%M"),
                }
            elif from_time and not to_time:
                entries = (
                    Entry.objects.all()
                    .filter(
                        start__gte=from_time,
                        user=request.user,
                        inactive=False,
                        end__isnull=False,
                    )
                    .order_by("-end")
                    .all()
                )
                initial_dict = {
                    "from_time": from_time.strftime("%Y-%m-%dT%H:%M"),
                }
            elif not from_time and to_time:
                entries = (
                    Entry.objects.all()
                    .filter(
                        start__lte=to_time,
                        user=request.user,
                        inactive=False,
                        end__isnull=False,
                    )
                    .order_by("-end")
                    .all()
                )
                initial_dict = {
                    "to_time": to_time.strftime("%Y-%m-%dT%H:%M"),
                }
            else:
                entries = (
                    Entry.objects.all()
                    .filter(user=request.user, inactive=False, end__isnull=False)
                    .order_by("-end")
                )
                initial_dict = {}
        else:
            messages.error(
                request, "Wprowadzono błędne dane! Popraw i spróbuj ponownie."
            )
    else:
        entries = (
            Entry.objects.all()
            .filter(user=request.user, inactive=False, end__isnull=False)
            .order_by("-end")
        )

    fields = ["id", "client__name", "start", "end", "duration"]
    entries = entries.values(*fields)
    entries_json = entries_to_json(list(entries))

    search_entries_form = SearchEntriesForm(initial=initial_dict)

    context = {
        "search_entries_form": search_entries_form,
        "entries_list": entries,
        "entries_json": entries_json,
    }
    return render(request, "entries/entries.html", context)


@login_required
def client_details(request, client_slug):
    client = Client.objects.filter(inactive=False).get(slug=client_slug)

    client_link = (
        f"https://maps.google.com/maps?q= {client.latitude},{client.longitude}"
    )
    context = {"client": client, "client_link": client_link}
    return render(request, "entries/client_details.html", context)


@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST" and request.user.is_authenticated:
        form = EditClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            messages.success(request, "Pomyślnie zapisano zmiany!")
            return HttpResponseRedirect(reverse("entries:clients"))
        messages.error(request, "Nie można zapisać zmian!")
    else:
        form = EditClientForm(instance=client)
    return render(
        request, "entries/client_edit.html", {"form": form, "client_details": client}
    )


@login_required
def client_add(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = EditClientForm(request.POST)
        if form.is_valid():
            Client.objects.create(**form.cleaned_data)
            messages.success(request, "Pomyślnie dodano klienta!")
            return HttpResponseRedirect(reverse("entries:clients"))
        messages.error(request, "Nie można zapisać zmian!")
    else:
        form = EditClientForm()
    return render(request, "entries/client_edit.html", {"form": form})


@login_required
def entry_save(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry.start.strftime("%Y-%m-%dT%H:%M"),
        "end": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }

    if request.method == "POST" and request.user.is_authenticated:
        active_entries = Entry.objects.filter(
            user=request.user, inactive=False, end__isnull=True
        )
        form = EditEntryForm(request.POST, instance=entry, initial=initial_dict)
        if form.is_valid():
            start_time = form.cleaned_data["start"]
            end_time = form.cleaned_data["end"]

            if len(active_entries) <= 1 and end_time is None:
                entry = form.save(commit=False)
                entry.duration = None
                entry.save()
                messages.success(request, "Pomyślnie zapisano zmiany!")
                return HttpResponseRedirect(reverse("main:home"))
            if end_time is not None and end_time >= start_time:
                entry = form.save(commit=False)
                entry.duration = end_time - start_time
                entry.save()
                messages.success(request, "Pomyślnie zakończono zadanie!")
                return HttpResponseRedirect(reverse("main:home"))
            if end_time is not None and end_time < start_time:
                messages.error(
                    request, "Data zakończenia musi być późniejsza od daty startu!"
                )
                return HttpResponseRedirect(
                    reverse("entries:entry_save", kwargs={"entry_id": entry_id})
                )
            else:
                messages.warning(request, "Błąd formularza!")
                return HttpResponseRedirect(
                    reverse("entries:entry_save", kwargs={"entry_id": entry_id})
                )
        else:
            messages.warning(request, "Błąd formularza!")
            return HttpResponseRedirect(
                reverse("entries:entry_save", kwargs={"entry_id": entry_id})
            )
    else:
        form = EditEntryForm(instance=entry, initial=initial_dict)

        context = {"entry_details": entry, "form": form}
        return render(request, "entries/entry_details.html", context)


@login_required
def entry_details(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry.start.strftime("%Y-%m-%dT%H:%M"),
        "end": entry.end.strftime("%Y-%m-%dT%H:%M"),
    }

    if request.method == "POST" and request.user.is_authenticated:
        active_entries = Entry.objects.filter(
            user=request.user, inactive=False, end__isnull=True
        )
        form = EditEntryForm(request.POST, instance=entry, initial=initial_dict)
        if form.is_valid():
            start_time = form.cleaned_data["start"]
            end_time = form.cleaned_data["end"]

            if len(active_entries) == 0 and end_time is None:
                entry = form.save(commit=False)
                entry.duration = None
                entry.save()
                messages.success(request, "Pomyślnie przywrócono zadanie!")
                return HttpResponseRedirect(reverse("main:home"))

            if len(active_entries) != 0 and end_time is None:
                messages.error(
                    request, "Nie można przywrócić zadania. Najpierw zakończ bieżące!"
                )
                return HttpResponseRedirect(
                    reverse("entries:entry_details", kwargs={"entry_id": entry_id})
                )

            if end_time is not None and end_time < start_time:
                messages.error(
                    request, "Data zakończenia musi być późniejsza od daty startu!"
                )
                return HttpResponseRedirect(
                    reverse("entries:entry_details", kwargs={"entry_id": entry_id})
                )

            if end_time is not None and end_time >= start_time:
                entry = form.save(commit=False)
                entry.duration = end_time - start_time
                entry.save()
                messages.success(request, "Pomyślnie zapisano zmiany!")
                return HttpResponseRedirect(reverse("entries:entries"))

        else:
            messages.warning(request, "Błąd formularza!")
            return HttpResponseRedirect(
                reverse("entries:entry_details", kwargs={"entry_id": entry_id})
            )
    else:
        form = EditEntryForm(instance=entry, initial=initial_dict)
        context = {"entry_details": entry, "form": form}

    return render(request, "entries/entry_details.html", context)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return datetime.fromtimestamp(o.timestamp()).isoformat(" ", "seconds")

        return json.JSONEncoder.default(self, o)


def entries_to_json(entries_list: list):
    i = 0
    for item in entries_list:
        item_id = item["id"]
        for key, value in item.items():
            if key in ("start", "end") and value is not None:
                value = datetime.fromtimestamp(value.timestamp()).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                entries_list[i][key] = value
        entries_list[i] = {
            key: f'<a href="/entries/entries/{item_id}">{value}</a>'
            for key, value in item.items()
        }
        i += 1
    return json.dumps(entries_list, cls=DateTimeEncoder)
