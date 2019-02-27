import time
import json
import scrapy

from urllib.parse import urlencode
from scrapy import Request

from fetchdata import settings
from fetchdata.items import StockItem
from fetchdata.utils import timestamp, trans_cookie


class StockSpider(scrapy.Spider):
    """股票列表采集"""
    name = 'stock_list'
    allowed_domains = ['xueqiu.com']

    def start_requests(self):
        per_page = settings.env('STOCK_LIST_PER_PAGE', cast=int)
        max_page = settings.env('STOCK_MAX_PAGES', cast=int)
        cookies = trans_cookie(settings.env('XUEQIU_COOKIES'))
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': settings.env('STOCK_LIST_API_REFERER'),
        }
        for page in range(1, max_page + 1):
            params = {
                'page': page,
                'size': per_page,
                'order': 'desc',
                'orderby': 'percent',
                'order_by': 'percent',
                'market': 'CN',
                'type': 'sh_sz',
                '_': timestamp(time.time()),
            }

            url = "%s?%s" % (settings.env('STOCK_LIST_API'), urlencode(params))

            yield Request(url, cookies=cookies, headers=headers)

    def parse(self, response):
        body = json.loads(response.body)

        for stock in body.get('data', {}).get('list', []):
            item = StockItem()
            item['name'] = stock.get('name')
            item['code'] = stock.get('symbol')

            yield item
