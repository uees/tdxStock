import json
from django.db import models

from tdxStock.fields import JSONField


class Option(models.Model):
    name = models.CharField('项目', max_length=200, unique=True)
    value = JSONField('值', null=True, blank=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    _options = None  # 缓存查询结果

    @classmethod
    def query_options(cls, names):
        if isinstance(names, str):
            names = [names, ]

        cls._options = cls.objects.filter(name__in=names).all()
        return cls._options

    @classmethod
    def get_option(cls, name, default=None):
        if not cls._options:
            raise Exception('Option.query_options(names) is not called, or option.query_options(names) returns nothing')

        for option in cls._options:
            if option.name == name:
                return option.value

        return default
