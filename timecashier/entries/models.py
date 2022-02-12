from django.db import models
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey("auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="clients")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'# {self.longitude} {self.latitude} {self.created} {self.modified}'

class Entry(models.Model):
    start = models.DateTimeField(auto_now_add=True) #default=make_aware(datetime.now(), get_current_timezone()))
    end = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="entries")
    user = models.ForeignKey("auth.User", on_delete=models.SET_DEFAULT, default=1, related_name="entries")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.client} {self.start} {self.end}'