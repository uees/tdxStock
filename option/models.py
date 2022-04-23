from django.db import models


class Option(models.Model):
    name = models.CharField('项目', max_length=200, unique=True)
    value = models.JSONField('值', null=True, blank=True)
    enable = models.BooleanField(default=True)

    class Meta:
        db_table = "options"
        verbose_name = '选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    _options = {}  # cache

    @classmethod
    def get_option(cls, name, default=None):
        if name in cls._options:
            return cls._options[name]

        o = cls.objects.filter(enable=True).filter(name=name).first()

        if o:
            cls._options[name] = o.value
            return o.value

        return default
