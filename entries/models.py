from datetime import date
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from main.models import Organization


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + "-" + get_random_string(length=4)
    return unique_slug


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
    street = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey(
        "auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="clients"
    )
    inactive = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="entries/logos/", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"  # {self.longitude} {self.latitude} {self.created} {self.modified}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super(Client, self).save(*args, **kwargs)


class ClientRate(Timestamped):
    name = models.CharField(max_length=50, default="general")
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client} {self.name} {self.rate}"


class Entry(Timestamped):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, related_name="entries"
    )
    user = models.ForeignKey(
        "auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="entries"
    )
    inactive = models.BooleanField(default=False)
    tags = models.ManyToManyField("tags.Tag", related_name="entries", blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_end_gte_start",
                check=models.Q(end__gte=models.F("start")),
            )
        ]

    def __str__(self):
        return f"{self.client} {self.start} {self.end}"


class Location(Timestamped):
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey(
        "auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="locations"
    )

    def __str__(self):
        return f"{self.created} {self.user} {self.latitude} {self.longitude}"
