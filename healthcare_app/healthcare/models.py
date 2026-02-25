from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name="created_at", db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated_at", db_index=True, auto_now=True)
    archived_stamp = models.DateTimeField(verbose_name="archived_stamp", null=True, blank=True)
