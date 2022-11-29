from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from .models import Client
from .models import Entry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "latitude", "longitude", "user", "created", "modified", "inactive"]
    search_fields = ["name"]
    list_filter = ["user", "inactive"]
    prepopulated_fields = {"slug": ("name",)}


class EntryResource(resources.ModelResource):
    class Meta:
        model = Entry


@admin.register(Entry)
class EntryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ["id", "start", "end", "client", "user", "created", "modified", "inactive"]
    search_fields = ["client"]
    list_filter = ["client", "user", "inactive"]
    resource_class = EntryResource
