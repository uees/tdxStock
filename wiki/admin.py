from django.contrib import admin
from django.db import models
from django.utils import timezone

from .models import Concept
from .widgets import MarkdownWidget


class ConceptAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MarkdownWidget}
    }

    def save_model(self, request, obj, form, change):
        obj.description_html = request.POST.get('description_html')
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(Concept, ConceptAdmin)
