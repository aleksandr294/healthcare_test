from django.utils import timezone

from celery_app import app
from visit.enums import VisitStatusChoices
from visit.models import Visit


@app.task
def check_visits() -> None:
    Visit.objects.filter(status=VisitStatusChoices.SCHEDULED, start_date_time__lt=timezone.now()).update(
        status=VisitStatusChoices.MISSED
    )
