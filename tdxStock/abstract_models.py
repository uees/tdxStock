from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    created_at = models.DateTimeField("创建时间", null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField("更新时间", null=True, blank=True)

    class Meta:
        abstract = True
