from django.contrib import admin

from healthcare.constants import BASE_FIELDS
from visit.models import Visit

# Register your models here.


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = BASE_FIELDS + ("number", "caregiver", "patient", "status")
    list_search = ("number", "caregiver", "patient")
    list_filter = ("status",)
