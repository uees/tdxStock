from urllib.parse import urlencode

import scrapy

from basedata.models import Stock

from .report import ReportSpider


class StockReportSpider(ReportSpider):
    name = 'stock_report'

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
            'Referer': self.referer.format(code=stock.code),
        }

        url = "%s?%s" % (self.api, urlencode(params))
        yield scrapy.Request(
            url,
            callback=self.parse,
            cookies=self.cookies,
            headers=headers,
            meta={"stock": stock}
        )
