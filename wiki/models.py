from django.db import models
from django.urls import reverse

from tdxStock.abstract_models import Timestamp


class Concept(Timestamp):
    """名词解释"""
    name = models.CharField("名称", max_length=200, unique=True)
    description = models.TextField("描述(Markdown)", null=True, blank=True)
    description_html = models.TextField("描述(HTML)", null=True, editable=False)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "概念"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_at'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        reverse('wiki:concept-detail', kwargs={'pk': self.id})
