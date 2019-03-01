# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models import Stock, Territory
from fetchdata.items import StockItem, TerritoryItem
from fetchdata.utils import get_params, string2dict


class TerritorySpiderSpider(scrapy.Spider):
    name = 'territory_spider'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/#HS']
    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    def parse(self, response):
        top_sel = response.xpath('//*[@id="f0-f5"]')

        for sel in top_sel.xpath('ul/li'):
            territory_name = sel.xpath('a/text()').get()
            if territory_name:
                item = TerritoryItem()
                item['name'] = territory_name.strip()

                territory, _ = Territory.objects.get_or_create(name=item['name'])

                yield item

                qcond = sel.xpath('./@qcond').get()
                qquery = sel.xpath('./@qquery').get()

                qcond = string2dict(qcond, eq=':')

                params = {
                    "type": "query",
                    "fields": "NO,SYMBOL,NAME,PRICE,PERCENT,UPDOWN,FIVE_MINUTE,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER,HS,LB,WB,ZF,PE,MCAP,TCAP,MFSUM,MFRATIO.MFRATIO2,MFRATIO.MFRATIO10,SNAME,CODE,ANNOUNMT,UVSNEWS",
                    "host": self.api,
                    "page": qcond['page'],
                    "query": qquery,
                    "sort": qcond['sort'],
                    "order": qcond['order'],
                    "count": qcond['count'],
                }

                url = "%s?%s" % (self.api, urlencode(params))
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"territory": item['name']})

    def parse_stocks(self, response):
        body = json.loads(response.body)
        stock_list = body.get('list', [])
        for stock in stock_list:
            item = StockItem()
            item['territory'] = response.meta['territory']
            item['name'] = stock.get('SNAME')
            item['code'] = stock.get('SYMBOL')

            Stock.objects.filter(code__endswith=item['code']).update(
                territory=Territory.objects.filter(name=item['territory']).first()
            )

            yield item

        params = get_params(response)
        pagecount = body.get('pagecount')
        if pagecount > 1:
            for page in range(1, pagecount):
                params.update({"page": page})

                url = "%s?%s" % (self.api, urlencode(params))
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"territory": response.meta['territory']})
