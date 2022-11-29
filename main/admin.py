from django.contrib import admin

from main.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = "TimeCashier Admin"
admin.site.site_title = "TimeCashier Admin Portal"
admin.site.index_title = "Witaj w portalu TimeCashier"
