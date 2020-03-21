from django.core.management import BaseCommand  # , CommandError
from django.db.models import Max

from basedata.models import Report, ReportType, Stock, XReport
from tdxStock.helpers import dict_merge


# 在一个 app 的 management/commands 目录下
# 内部需要定义一个 Command 类并继承 BaseCommand 类或其子类
# python manage.py update_last_report_date --single
class Command(BaseCommand):
    help = '更新股票的后报表期字段'

    # add_arguments 函数是用来接收可选参数的
    def add_arguments(self, parser):
        parser.add_argument('--single',
                            action='store_true',
                            dest='single',
                            default=False,
                            help='是否单季度报告')

    def handle(self, *args, **options):
        if options['single']:
            report_model = Report
            key = "last_report_date"
        else:
            report_model = XReport
            key = "last_all_report_date"

        reports = report_model.objects.values('stock_id', 'report_type_id').annotate(last_date=Max('report_date'))
        for report in reports:
            stock = Stock.objects.get(pk=report['stock_id'])
            report_type = ReportType.objects.get(pk=report['report_type_id'])

            metas = stock.metas if stock.metas else {}
            dict_merge(metas, {report_type.slug: {key: report['last_date']}})
            stock.metas = metas

            stock.save()

        self.stdout.write(self.style.SUCCESS('success!'))
