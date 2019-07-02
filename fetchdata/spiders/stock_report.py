from django.db.models import Max

from basedata.models import Report, Stock, XReport

from fetchdata.spiders.report import ReportSpider


class StockReportSpider(ReportSpider):
    """采用单个股票的报表，主要用于修复数据"""
    name = 'stock_report'

    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.code = code

    def closed(self, spider):
        # 关闭时更新最后报表日期
        if self.is_single_quarter:
            report = Report.objects.filter(code=self.code).aggregate(Max('report_date'))
            Stock.objects.filter(code=self.code).update(last_report_date=report['report_date__max'])
        else:
            report = XReport.objects.filter(code=self.code).aggregate(Max('report_date'))
            Stock.objects.filter(code=self.code).update(last_all_report_date=report['report_date__max'])

    def start_requests(self):
        stock = Stock.objects.get(code=self.code)
        yield self.make_request(stock)
