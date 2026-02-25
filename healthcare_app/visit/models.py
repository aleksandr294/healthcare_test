from django.contrib.postgres.indexes import GinIndex
from django.db import models

from healthcare.models import BaseModel
from visit.enums import VisitStatusChoices

# Create your models here.


class Visit(BaseModel):
    number = models.CharField(max_length=10, unique=True)
    caregiver = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="caregiver_visits")
    patient = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="patient_visits")

    duties = models.ManyToManyField("duty.Duty")
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    status = models.CharField(choices=VisitStatusChoices.choices, default=VisitStatusChoices.SCHEDULED)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "visits"
        indexes = [
            models.Index(fields=["status", "start_date_time"], name="idx_status_start"),
            GinIndex(
                fields=["number"],
                name="ix_number_trgm",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.number
