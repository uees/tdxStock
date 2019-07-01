# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models.category import Industry
from fetchdata.utils import get_params, string2dict


class ZJHIndustrySpider(scrapy.Spider):
    name = 'industry_zjh'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/']

    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    type = "证监会分类"

    def stock_list_request(self, industry_id, params):
        url = "%s?%s" % (self.api, urlencode(params))

        # meta 传 industry_id 唯一字段
        return scrapy.Request(
            url,
            headers=self.headers,
            callback=self.parse_stocks,
            meta={"industry_id": industry_id}
        )

    def parse(self, response):
        # Spider must return Request, BaseItem, dict or None
        industry_sel = response.xpath('//*[@id="f0-f7"]')

        # 一级
        data = dict(
            name=industry_sel.xpath('a/text()').get(),
            type=self.type,
            level=1
        )

        # 行业表数据的创建会阻塞，因数据量少可以接受阻塞
        first_industry, _ = Industry.objects.get_or_create(**data)

        # 二级
        for second_sel in industry_sel.xpath('ul/li'):
            second_industry, _ = Industry.objects.get_or_create(
                name=second_sel.xpath('a/text()').get(),
                parent=first_industry,
                type=self.type,
                level=2
            )

            # 三级
            for third_sel in second_sel.xpath('ul/li'):
                third_industry, _ = Industry.objects.get_or_create(
                    name=third_sel.xpath('a/text()').get(),
                    parent=second_industry,
                    type=self.type,
                    level=3
                )

                qcond = third_sel.xpath('./@qcond').get()
                qcond = string2dict(qcond, eq=':')

                qquery = third_sel.xpath('./@qquery').get()

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

                yield self.stock_list_request(third_industry.id, params)

    def parse_stocks(self, response):
        body = json.loads(response.body)

        stock_list = body.get('list', [])
        for stock in stock_list:
            yield dict(
                name=stock.get('SNAME'),
                code=stock.get('SYMBOL'),
                industry_id=response.meta['industry_id']
            )

        params = get_params(response)
        pagecount = int(body.get('pagecount'))
        page = int(params['page'])
        if pagecount > page:
            params.update({"page": page + 1})
            yield self.stock_list_request(response.meta['industry_id'], params)
