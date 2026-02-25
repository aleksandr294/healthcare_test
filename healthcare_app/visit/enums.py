from django.db.models import TextChoices


class VisitStatusChoices(TextChoices):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"
    MISSED = "missed"
