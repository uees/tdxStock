# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models.category import Industry, IndustryStock
from basedata.models.stock import Stock
from fetchdata.utils import string2dict, get_params
from fetchdata.items import IndustryItem, StockItem


class IndustrySpiderSpider(scrapy.Spider):
    name = 'industry_spider'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/']

    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    def parse(self, response):
        # Spider must return Request, BaseItem, dict or None
        industry_sel = response.xpath('//*[@id="f0-f7"]')

        # 一级
        top_item = IndustryItem()
        top_item['name'] = industry_sel.xpath('a/text()').get()

        first_industry, _ = Industry.objects.get_or_create(name=top_item['name'])

        yield top_item

        # 二级
        for second_sel in industry_sel.xpath('ul/li'):
            second_item = IndustryItem()
            second_item['parent'] = top_item['name']
            second_item['name'] = second_sel.xpath('a/text()').get()

            second_industry, _ = Industry.objects.get_or_create(
                name=second_item['name'],
                parent=first_industry
            )

            yield second_item

            # 三级
            for third_sel in second_sel.xpath('ul/li'):
                third_item = IndustryItem()
                third_item['parent'] = second_item['name']
                third_item['name'] = third_sel.xpath('a/text()').get()

                third_industry, _ = Industry.objects.get_or_create(
                    name=third_item['name'],
                    parent=second_industry
                )

                yield third_item

                qcond = third_sel.xpath('./@qcond').get()
                qquery = third_sel.xpath('./@qquery').get()

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
                                     meta={"industry": third_item['name']})

    def parse_stocks(self, response):
        body = json.loads(response.body)

        stock_list = body.get('list', [])
        for stock in stock_list:
            item = StockItem()
            item['industry'] = response.meta['industry']
            item['name'] = stock.get('SNAME')
            item['code'] = stock.get('SYMBOL')

            stock_obj = Stock.objects.filter(code__endswith=item['code']).first()
            industry_obj = Industry.objects.filter(name=item['industry']).first()

            if stock_obj and industry_obj:
                IndustryStock.objects.get_or_create(
                    stock=stock_obj,
                    industry=industry_obj
                )

            yield item

        params = get_params(response)
        pagecount = body.get('pagecount')
        if pagecount > 1:
            for page in range(1, pagecount):
                params.update({"page": page})

                url = "%s?%s" % (self.api, urlencode(params))
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"industry": response.meta['industry']})

