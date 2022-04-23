import json
from urllib.parse import urlencode

import scrapy

from basedata.models import Concept
from collector.utils import get_params
from tdxStock.helpers import string2dict


class ConceptSpider(scrapy.Spider):
    name = 'concept'
    allowed_domains = ['163.com']
    start_urls = ['http://quotes.money.163.com/old/']
    api = 'http://quotes.money.163.com/hs/service/diyrank.php'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://quotes.money.163.com/old/',
    }

    def stock_list_request(self, concept_id, params):
        url = "%s?%s" % (self.api, urlencode(params))
        return scrapy.Request(
            url,
            headers=self.headers,
            callback=self.parse_stocks,
            meta={"concept_id": concept_id}
        )

    def parse(self, response):
        top_sel = response.xpath('//*[@id="f0-f4"]')

        for sel in top_sel.xpath('ul/li'):
            name = sel.xpath('a/text()').get()
            if name:
                # 这里数据量少, 允许阻塞
                concept, _ = Concept.objects.get_or_create(name=name.strip())

                qcond = sel.xpath('./@qcond').get()
                qcond = string2dict(qcond, eq=':')

                qquery = sel.xpath('./@qquery').get()

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

                yield self.stock_list_request(concept.id, params)

    def parse_stocks(self, response):
        body = json.loads(response.body)
        concept_id = response.meta['concept_id']
        stock_list = body.get('list', [])
        for stock in stock_list:
            yield {
                'concept_id': concept_id,
                'name': stock.get('SNAME'),
                'code': stock.get('SYMBOL')
            }

        params = get_params(response)
        pagecount = int(body.get('pagecount'))
        page = int(params['page'])
        if pagecount > page:
            params.update({"page": page + 1})
            yield self.stock_list_request(concept_id, params)
