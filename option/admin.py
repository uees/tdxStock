from django.contrib import admin
from django_extensions.db.fields.json import JSONField
from .models import Option
from django.conf import settings


class OptionAdmin(admin.ModelAdmin):
    list_max_show_all = 20
    list_per_page = 20

    fieldsets = [
        ('项目', {'fields': ['name']}),
        ('值', {'fields': ['value']}),
        ('开关', {'fields': ['enable']}),
    ]


admin.site.register(Option, OptionAdmin)
