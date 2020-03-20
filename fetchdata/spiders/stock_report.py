from basedata.models import Report, Stock, XReport

from fetchdata.spiders.report import ReportSpider


class StockReportSpider(ReportSpider):
    """采用单个股票的报表，主要用于修复数据"""
    name = 'stock_report'

    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.code = code
        self.crawl_mode = 'all'  # 强制全量采集

    def start_requests(self):
        stock = Stock.objects.get(code=self.code)
        yield self.make_request(stock)
