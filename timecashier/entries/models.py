from django.db import models
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime, date, timedelta

# Create your models here.


class ChceckAgeMixin:
    def is_from_current_week(self):
        current_date = date.today()
        week_start = current_date - timedelta(days=current_date.weekday())
        week_start_datetime = datetime.combine(week_start, datetime.min.time())
        return self.start > week_start_datetime

    def was_created_in_last_n_days(self, n=1):
        delta = timedelta(days=n)
        return datetime.now() - self.created < delta


class Timestamped(models.Model, ChceckAgeMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # hej django ta klasa jest tylko po to zeby po niej dziedziczyc, nie tworz mi takiej tabeli:
    class Meta:
        abstract = True


class Client(Timestamped):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey("auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="clients")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'# {self.longitude} {self.latitude} {self.created} {self.modified}'


class Entry(Timestamped):
    start = models.DateTimeField(auto_now_add=True) #default=make_aware(datetime.now(), get_current_timezone()))
    end = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="entries")
    user = models.ForeignKey("auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="entries")
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField("tags.Tag", related_name="entries")

    def __str__(self):
        return f'{self.client} {self.start} {self.end}'