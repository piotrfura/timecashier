import json
from datetime import datetime
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from entries.forms import EditClientForm
from entries.forms import EditEntryForm
from entries.forms import NewEntryForm
from entries.forms import SearchEntriesForm
from entries.models import Client
from entries.models import Entry
from entries.models import Location
from main.models import OrganizationUser

# from entries.models import ClientRate


def get_user_org(request):
    user = get_object_or_404(OrganizationUser, user=request.user)
    return user.organization


@login_required
def home(request):
    organization = get_user_org(request)

    session = Session.objects.get(session_key=request.session.session_key)
    session_data = session.get_decoded()
    nearest_client = session_data.get("nearest_client")

    entries = (
        Entry.objects.filter(user=request.user, inactive=False, end__isnull=False)
        .order_by("-end")
        .all()[0:5]
    )
    active_entry = Entry.objects.filter(
        user=request.user, inactive=False, end__isnull=True
    ).order_by("-start")[:1]
    initial_dict = {
        "client": nearest_client,
        "start": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }
    if (
        request.method == "POST"
        and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.user.is_authenticated
    ):
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        Location.objects.create(
            longitude=longitude, latitude=latitude, user=request.user
        )

    if request.method == "POST" and request.user.is_authenticated:
        form = NewEntryForm(request.POST, organization=organization)
        if form.is_valid() and len(active_entry) == 0:
            form.cleaned_data["user"] = request.user
            start_time = form.cleaned_data["start"]
            end_time = form.cleaned_data["end"]
            if end_time is None:
                Entry.objects.create(**form.cleaned_data)
                messages.success(request, "Pomyślnie rozpoczęto nowe zadanie!")
            if end_time is not None and end_time >= start_time:
                form.cleaned_data["duration"] = end_time - start_time
                Entry.objects.create(**form.cleaned_data)
                messages.success(request, "Pomyślnie dodano zadanie!")
            if end_time is not None and end_time < start_time:
                messages.error(
                    request, "Data zakończenia musi być późniejsza od daty startu!"
                )
            return HttpResponseRedirect(reverse("entries:home"))
        if len(active_entry) != 0:
            messages.error(
                request, "Przed dodaniem kolejnego zadania musisz zakończyć poprzednie!"
            )

    else:
        form = NewEntryForm(initial=initial_dict, organization=organization)

    fields = ["id", "client__name", "start", "end", "duration"]
    entries = entries.values(*fields)
    entries_list = list(entries)
    entries_list.reverse()
    entries_json = entries_to_json(entries_list)

    context = {
        "form": form,
        "active_entry": active_entry,
        "entries_json": entries_json,
    }

    return render(request, "entries/home.html", context)


@login_required
def client_nearby(request):
    clients = Client.objects.filter(inactive=False, organization=get_user_org(request))
    clients_dist = {}

    longitude = request.GET.get("longitude")
    latitude = request.GET.get("latitude")

    for client in clients:
        length = abs(
            (
                (float(client.longitude) - float(longitude)) ** 2
                + (float(client.latitude) - float(latitude)) ** 2
            )
            ** (0.5)
        )
        clients_dist[client] = length
    min_dist = min(clients_dist.values())
    nearest_client = [
        client for client in clients_dist if clients_dist[client] == min_dist
    ][0]

    request.session["nearest_client"] = nearest_client.id

    data = {"nearest_client": nearest_client.id}
    return JsonResponse(data)


@login_required
def clients_list(request):
    organization = get_user_org(request)
    if organization:
        clients = Client.objects.filter(
            inactive=False, organization=get_user_org(request)
        ).all()
        fields = ["id", "name", "latitude", "longitude"]
        clients = clients.values(*fields)
        clients_json = clients_to_json(list(clients))
    else:
        clients_json = {}

    context = {"clients_json": clients_json}
    return render(request, "entries/clients.html", context)


@login_required
def entries_list(request, month=0):
    organization = get_user_org(request)
    month_start_time = datetime.today().replace(
        month=datetime.today().month + 1 - month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    init_to_time = month_start_time - timedelta(microseconds=1)
    init_from_time = month_start_time - timedelta(days=init_to_time.day)

    initial_dict = {
        "from_time": init_from_time.strftime("%Y-%m-%dT%H:%M"),
        "to_time": init_to_time.strftime("%Y-%m-%dT%H:%M"),
    }
    if request.method == "POST":
        search_session_form = SearchEntriesForm(request.POST, organization=organization)
        if search_session_form.is_valid():
            client = search_session_form.cleaned_data["client"]
            from_time = search_session_form.cleaned_data["from_time"]
            to_time = search_session_form.cleaned_data["to_time"]

            entry_filters = {
                "user": request.user,
                "end__isnull": False,
            }

            if client:
                entry_filters["client"] = client
            if from_time:
                entry_filters["start__gte"] = from_time
                from_time = from_time.strftime("%Y-%m-%dT%H:%M")
            if to_time:
                entry_filters["start__lte"] = to_time
                to_time = to_time.strftime("%Y-%m-%dT%H:%M")

            entries = (
                Entry.objects.all()
                .filter(*[Q(**{k: v}) for k, v in entry_filters.items() if v])
                .filter(inactive=False)
                .order_by("-end")
                .all()
            )
            initial_dict = {
                "client": client,
                "from_time": from_time,
                "to_time": to_time,
            }
        else:
            messages.error(
                request, "Wprowadzono błędne dane! Popraw i spróbuj ponownie."
            )
    else:
        entries = (
            Entry.objects.all()
            .filter(
                start__range=(init_from_time, init_to_time),
                user=request.user,
                inactive=False,
                end__isnull=False,
            )
            .order_by("-end")
        )
    fields = ["id", "client__name", "start", "end", "duration"]
    entries = entries.values(*fields)
    entries_list = list(entries)
    entries_list.reverse()
    entries_json = entries_to_json(entries_list)

    search_entries_form = SearchEntriesForm(
        initial=initial_dict, organization=organization
    )
    context = {
        "search_entries_form": search_entries_form,
        "entries_list": entries,
        "entries_json": entries_json,
    }
    return render(request, "entries/entries.html", context)


@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    # client_rates = ClientRate.objects.filter(client_id=client.pk).all()
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

    client_link = (
        f"https://maps.google.com/maps?q= {client.latitude},{client.longitude}"
    )
    context = {
        "form": form,
        "client_details": client,
        # "client_rates": client_rates,
        "client_lat": client.latitude,
        "client_long": client.longitude,
        "client_link": client_link,
    }
    return render(request, "entries/client_edit.html", context)


@login_required
def client_add(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = EditClientForm(request.POST)
        if form.is_valid():
            Client.objects.create(
                organization=get_user_org(request), **form.cleaned_data
            )
            messages.success(request, "Pomyślnie dodano klienta!")
            return HttpResponseRedirect(reverse("entries:clients"))
        messages.error(request, "Nie można zapisać zmian!")
    else:
        form = EditClientForm()
    return render(request, "entries/client_edit.html", {"form": form})


@login_required
def client_delete(request, client_id):
    if request.method == "POST" and request.user.is_authenticated:
        client = get_object_or_404(Client, pk=client_id)
        if client.organization == get_user_org(request):
            client.inactive = True
            client.save()
            messages.success(request, "Pomyślnie usunięto klienta!")
        else:
            messages.error(request, "Nie można zapisać zmian!")
    return HttpResponseRedirect(reverse("entries:clients"))


@login_required
def entry_save(request, entry_id):
    organization = get_user_org(request)
    entry = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry.start.strftime("%Y-%m-%dT%H:%M"),
        "end": datetime.now().strftime("%Y-%m-%dT%H:%M"),
    }

    if request.method == "POST" and request.user.is_authenticated:
        active_entries = Entry.objects.filter(
            user=request.user, inactive=False, end__isnull=True
        )
        form = EditEntryForm(
            request.POST,
            instance=entry,
            initial=initial_dict,
            organization=organization,
        )
        if form.is_valid():
            start_time = form.cleaned_data["start"]
            end_time = form.cleaned_data["end"]

            if len(active_entries) <= 1 and end_time is None:
                entry = form.save(commit=False)
                entry.duration = None
                entry.save()
                messages.success(request, "Pomyślnie zapisano zmiany!")
                return HttpResponseRedirect(reverse("entries:home"))
            if end_time is not None and end_time >= start_time:
                entry = form.save(commit=False)
                entry.duration = end_time - start_time
                entry.save()
                messages.success(request, "Pomyślnie zakończono zadanie!")
                return HttpResponseRedirect(reverse("entries:home"))
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
        form = EditEntryForm(
            instance=entry, initial=initial_dict, organization=organization
        )

        context = {"entry_details": entry, "form": form}
        return render(request, "entries/entry_details.html", context)


@login_required
def entry_details(request, entry_id):
    organization = get_user_org(request)
    entry = get_object_or_404(Entry, pk=entry_id)
    initial_dict = {
        "start": entry.start.strftime("%Y-%m-%dT%H:%M"),
        "end": entry.end.strftime("%Y-%m-%dT%H:%M"),
    }

    if request.method == "POST" and request.user.is_authenticated:
        active_entries = Entry.objects.filter(
            user=request.user, inactive=False, end__isnull=True
        )
        form = EditEntryForm(
            request.POST,
            instance=entry,
            initial=initial_dict,
            organization=organization,
        )
        if form.is_valid():
            start_time = form.cleaned_data["start"]
            end_time = form.cleaned_data["end"]

            if len(active_entries) == 0 and end_time is None:
                entry = form.save(commit=False)
                entry.duration = None
                entry.save()
                messages.success(request, "Pomyślnie przywrócono zadanie!")
                return HttpResponseRedirect(reverse("entries:home"))

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
        form = EditEntryForm(
            instance=entry, initial=initial_dict, organization=organization
        )
        context = {"entry_details": entry, "form": form}

    return render(request, "entries/entry_details.html", context)


@login_required
def entry_delete(request, entry_id):
    if request.method == "POST" and request.user.is_authenticated:
        entry = get_object_or_404(Entry, pk=entry_id)
        if entry.client.organization == get_user_org(request):
            entry.inactive = True
            entry.save()
            messages.success(request, "Pomyślnie usunięto zadanie!")
        else:
            messages.error(request, "Nie można zapisać zmian!")
    return HttpResponseRedirect(reverse("entries:entries"))


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
            elif key == "id" and value is not None:
                value = i + 1
                entries_list[i][key] = value
        entries_list[i] = {
            key: f'<a href="/entries/{item_id}">{value}</a>'
            for key, value in item.items()
        }
        i += 1
    entries_list.reverse()
    return json.dumps(entries_list, cls=DateTimeEncoder)


def clients_to_json(data_list: list):
    i = 0
    for item in data_list:
        item_id = item["id"]
        data_list[i] = {
            key: f'<a href="/clients/edit/{item_id}">{value}</a>'
            for key, value in item.items()
        }
        i += 1
    return json.dumps(data_list, cls=DateTimeEncoder)
