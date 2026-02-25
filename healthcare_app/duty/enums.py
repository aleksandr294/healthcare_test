from django.db.models import TextChoices


class DutyResultStatusChoices(TextChoices):
    DONE = "done"
    NOT_DONE = "not_done"
