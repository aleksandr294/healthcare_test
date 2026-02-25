from django.db import models

from duty.enums import DutyResultStatusChoices
from healthcare.models import BaseModel

# Create your models here.


class Duty(BaseModel):
    name = models.CharField(max_length=100)
    duration = models.DurationField()

    class Meta:
        db_table = "duties"

    def __str__(self):
        return self.name


class DutyResult(BaseModel):
    visit = models.ForeignKey("visit.Visit", on_delete=models.CASCADE, related_name="duty_results")
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    status = models.CharField(choices=DutyResultStatusChoices.choices)

    class Meta:
        db_table = "duty_results"
