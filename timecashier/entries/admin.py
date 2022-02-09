from django.contrib import admin
from .models import Client
from .models import Entry

# Register your models here.
# admin.site.register(Client)
# admin.site.register(Entry)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "latitude", "longitude", "created", "modified", "active"]
    search_fields = ["name"]
    list_filter = ["name", "active"]

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Entry._meta.get_fields()]

    pass