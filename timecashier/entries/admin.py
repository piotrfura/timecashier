from django.contrib import admin
from .models import Client
from .models import Entry

# Register your models here.
admin.site.register(Client)
admin.site.register(Entry)
