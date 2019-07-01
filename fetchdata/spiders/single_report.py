from urllib.parse import urlencode

import scrapy

from basedata.models import Stock
from fetchdata import settings

from .report import ReportSpider


class SingleReportSpider(ReportSpider):
    name = 'single_report'

    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.code = code

    def start_requests(self):
        stock = Stock.objects.get(code=self.code)
        params = {
            "symbol": stock.code,
            "type": self.type,
            "is_detail": True,
            "count": 5,
            "timestamp": "",
        }

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': settings.env('STOCK_DETAIL_API_REFERER').format(code=stock.code),
        }

        url = "%s?%s" % (self.api.format(report=getattr(self, 'report')), urlencode(params))
        yield scrapy.Request(url, self.parse, cookies=self.cookies, headers=headers, meta={
            "stock": stock,
        })
