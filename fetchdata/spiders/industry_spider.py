# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models.category import Industry, IndustryStock
from basedata.models.stock import Stock
from fetchdata.items import IndustryItem, StockItem
from fetchdata.utils import get_params, string2dict


class IndustrySpiderSpider(scrapy.Spider):
    name = 'industry_spider'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/']

    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    type = "证监会分类"

    def parse(self, response):
        # Spider must return Request, BaseItem, dict or None
        industry_sel = response.xpath('//*[@id="f0-f7"]')

        # 一级
        data = dict(
            name=industry_sel.xpath('a/text()').get(),
            type=self.type,
            level=1
        )
        top_item = IndustryItem(**data)
        first_industry, _ = Industry.objects.get_or_create(**data)

        yield top_item

        # 二级
        for second_sel in industry_sel.xpath('ul/li'):
            second_item = IndustryItem()
            second_item['parent'] = top_item['name']
            second_item['name'] = second_sel.xpath('a/text()').get()
            second_item['level'] = 2
            second_item['type'] = self.type

            second_industry, _ = Industry.objects.get_or_create(
                name=second_item['name'],
                parent=first_industry,
                type=self.type,
                level=second_item['level']
            )

            yield second_item

            # 三级
            for third_sel in second_sel.xpath('ul/li'):
                third_item = IndustryItem()
                third_item['parent'] = second_item['name']
                third_item['name'] = third_sel.xpath('a/text()').get()
                second_item['level'] = 3
                second_item['type'] = self.type

                third_industry, _ = Industry.objects.get_or_create(
                    name=third_item['name'],
                    parent=second_industry,
                    type=self.type,
                    level=second_item['level']
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

                # meta 传 industry_id 唯一字段
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"industry_id": third_industry.id})

    def parse_stocks(self, response):
        body = json.loads(response.body)

        industry = Industry.objects.filter(id=response.meta['industry_id']).first()

        stock_list = body.get('list', [])
        for stock in stock_list:
            item = StockItem()
            item['name'] = stock.get('SNAME')
            item['code'] = stock.get('SYMBOL')

            stock = Stock.objects.filter(code__endswith=item['code']).first()

            if stock and industry:
                IndustryStock.objects.get_or_create(
                    stock=stock,
                    industry=industry
                )

            yield item

        params = get_params(response)
        pagecount = body.get('pagecount')
        if pagecount > 1:
            for page in range(1, pagecount):
                params.update({"page": page})

                url = "%s?%s" % (self.api, urlencode(params))
                # scrapy.Request 对网址会自动去重
                yield scrapy.Request(url, headers=self.headers, callback=self.parse_stocks,
                                     meta={"industry_id": response.meta['industry_id']})
