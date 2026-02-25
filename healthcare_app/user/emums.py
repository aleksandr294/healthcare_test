from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    CAREGIVER = "caregiver"
    PATIENT = "patient"
    ADMIN = "admin"
