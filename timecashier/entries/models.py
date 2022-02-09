from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.longitude} {self.latitude} {self.created} {self.modified}'

class Entry(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.client} {self.start} {self.end}'