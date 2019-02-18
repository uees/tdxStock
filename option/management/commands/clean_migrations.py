import os
import shutil

from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = '清除 migrations 数据'

    def handle(self, *args, **options):
        clean_migrations()
        self.stdout.write(self.style.SUCCESS('清除成功'))


def clean_migrations():
    for migrations_path in get_migrations_dirs():
        for item in os.listdir(migrations_path):
            if item != '__init__.py':
                item_path = os.path.join(migrations_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path)


def get_migrations_dirs():
    migrations_dirs = []
    for item in os.listdir(settings.BASE_DIR):
        item_path = os.path.join(settings.BASE_DIR, item)
        if os.path.isdir(item_path):
            app_migrations_path = os.path.join(item_path, 'migrations')
            if os.path.exists(app_migrations_path):
                migrations_dirs.append(app_migrations_path)
    return migrations_dirs
