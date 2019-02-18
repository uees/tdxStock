from django.core.management import BaseCommand, CommandError

from option.models import Option


class Command(BaseCommand):
    help = '填充 options 表'

    def handle(self, *args, **options):
        if not Option.objects.exists():
            Option.objects.create(name="site_name", value='TdxStock')
            Option.objects.create(name="site_host", value='localhost')
            Option.objects.create(name="site_description", value='沪深股票分析')
            Option.objects.create(name="test", value={'a': 1, 'b': None, 'c': 'abc'})
            options = [Option(name=name, value=None) for name in ['site_seo_description', 'site_keywords',
                                                                  'open_site_comment', 'beian_code',
                                                                  'gongan_beian_code', 'show_gongan_code']]
            Option.objects.bulk_create(options)
            self.stdout.write(self.style.SUCCESS('填充 options 表成功'))

        else:
            raise CommandError('options 表中已经有数据')
