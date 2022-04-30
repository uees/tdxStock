from django.core.management import BaseCommand
from xpinyin import Pinyin

from basedata.models import Stock


# python manage.py update_stocks_pinyin
class Command(BaseCommand):
    help = '更新股票的 PINYIN 字段'

    def handle(self, *args, **options):
        p = Pinyin()

        for stock in Stock.objects.all():
            stock.pinyin = p.get_initials(stock.name, '')
            stock.save()

        self.stdout.write(self.style.SUCCESS('success!'))
