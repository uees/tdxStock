# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models import Concept, Stock, ConceptStock
from fetchdata.items import ConceptItem, StockItem
from fetchdata.utils import string2dict, get_params


class ConceptSpiderSpider(scrapy.Spider):
    name = 'concept_spider'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/']
    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    def parse(self, response):
        top_sel = response.xpath('//*[@id="f0-f4"]')

        for sel in top_sel.xpath('ul/li'):
            name = sel.xpath('a/text()').get()
            if name:
                item = ConceptItem()
                item['name'] = name.strip()

                concept, _ = Concept.objects.get_or_create(name=item['name'])

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
                                     meta={"concept": item['name']})

    def parse_stocks(self, response):
        body = json.loads(response.body)

        stock_list = body.get('list', [])
        for stock in stock_list:
            item = StockItem()
            item['concept'] = response.meta['concept']
            item['name'] = stock.get('SNAME')
            item['code'] = stock.get('SYMBOL')

            stock_obj = Stock.objects.filter(code__endswith=item['code']).first()
            concept_obj = Concept.objects.filter(name=item['concept']).first()

            if stock_obj and concept_obj:
                ConceptStock.objects.get_or_create(
                    stock=stock_obj,
                    concept=concept_obj
                )

            yield item

        params = get_params(response)
        pagecount = body.get('pagecount')
        if pagecount > 1:
            for page in range(1, pagecount):
                params.update({"page": page})

                url = "%s?%s" % (self.api, urlencode(params))
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"concept": response.meta['concept']})
