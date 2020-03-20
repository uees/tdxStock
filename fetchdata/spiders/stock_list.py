import json
import time
from urllib.parse import urlencode

import scrapy

from fetchdata.items import StockItem
from fetchdata.utils import timestamp, get_params
from tdxStock.helpers import read_cookie


class StockSpider(scrapy.Spider):
    """股票列表采集"""
    name = 'stock_list'
    allowed_domains = ['xueqiu.com']

    api = "https://xueqiu.com/service/v5/stock/screener/quote/list"
    per_page = 90
    cookies = read_cookie("xueqiu")
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': "https://xueqiu.com/hq",
    }

    def start_requests(self):
        yield self.stock_list_request(page=1, per_page=self.per_page)

    def stock_list_request(self, page, per_page):
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

        url = "%s?%s" % (self.api, urlencode(params))

        return scrapy.Request(
            url,
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        body = json.loads(response.body)
        data = body.get('data', {})
        count = int(data.get('count', 0))

        params = get_params(response)
        page = int(params['page'])
        per_page = int(params['size'])

        if page * per_page < count:
            yield self.stock_list_request(page + 1, per_page)

        for stock in data.get('list', []):
            item = StockItem()
            item['name'] = stock.get('name')
            item['code'] = stock.get('symbol')

            yield item
