from django.contrib import admin

from duty.models import Duty, DutyResult
from healthcare.constants import BASE_FIELDS

# Register your models here.


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = BASE_FIELDS + ("name", "duration")


@admin.register(DutyResult)
class DutyResultAdmin(admin.ModelAdmin):
    list_display = BASE_FIELDS + ("visit", "duty", "status")
    search_fields = ("visit",)
    list_filter = ("duty", "status")
