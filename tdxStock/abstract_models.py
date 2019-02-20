from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    created_at = models.DateTimeField("创建时间", null=True, editable=False, default=timezone.now)
    updated_at = models.DateTimeField("更新时间", null=True, editable=False, auto_now=True)  # 调用 save() 会自动更新, 调用 objects.update 不会更新

    class Meta:
        abstract = True
