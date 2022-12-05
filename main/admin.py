from django.contrib import admin

from main.models import Organization
from main.models import OrganizationAddress
from main.models import OrganizationUser
from main.models import OrganizationUserRole


admin.site.site_header = "TimeCashier Admin"
admin.site.site_title = "TimeCashier Admin Portal"
admin.site.index_title = "Witaj w portalu TimeCashier"


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(OrganizationAddress)
class OrganizationAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "street",
        "number",
        "zip_code",
        "city",
        "organization",
    )
    list_filter = ("organization",)


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "user")
    list_filter = ("organization", "user")


@admin.register(OrganizationUserRole)
class OrganizationUserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role")
    list_filter = ("user",)
