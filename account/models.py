import base64

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .identicon import Generator


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=100, blank=True)
    avatar = models.TextField('头像', null=True)
    updated_at = models.DateTimeField('更新时间', default=timezone.now)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.change_avatar()
        super().save(*args, **kwargs)

    def change_avatar(self):
        g = Generator(9, 9, foreground=settings.IDENTICON_FOREGROUND)
        data = base64.b64encode(g.generate(self.email, 256, 256, output_format='gif'))
        self.avatar = 'data:image/gif;base64,%s' % data
