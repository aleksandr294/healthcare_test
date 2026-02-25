from django.contrib import admin

from healthcare.constants import BASE_FIELDS
from user.models import User

# Register your models here.


@admin.register(User)
class DutyAdmin(admin.ModelAdmin):
    list_display = BASE_FIELDS + ("email", "full_name", "role")
