from datetime import datetime
from datetime import timedelta

from django.utils.timezone import get_current_timezone
from django.utils.timezone import make_aware
from faker import Faker

from .models import Client
from .models import Entry


def create_entries(n: int):
    fake = Faker('pl_PL')
    clients = Client.objects.all()
    for _ in range(0, n):
        now = make_aware(datetime.now(), get_current_timezone())
        start = fake.date_time_between(start_date=now + timedelta(days=-365))
        end = start + timedelta(minutes=fake.random_int(min=1, max=360))
        Entry.objects.create(
            start=start,
            end=end,
            client=fake.random_element(clients),
            active=fake.boolean(),
            created=start
        )
