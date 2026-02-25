#!/usr/bin/env python
import os
from typing import Any

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthcare.settings")

app = Celery("healthcare_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.task_track_started = True


@app.task(bind=True)
def debug_task(self: Any) -> None:
    print(f"Request: {self.request!r}")
