import json
import time
from urllib.parse import urlencode

import scrapy
from selenium import webdriver

from basedata.models import Industry, Stock, IndustryStock
from fetchdata import settings
from fetchdata.utils import timestamp, trans_cookie
from fetchdata.items import IndustryItem, StockItem


class XueqiuTerritorySpider(scrapy.Spider):
    name = 'xueqiu_territory'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/hq']
    type = "申万行业分类"
    api = "https://xueqiu.com/service/v5/stock/screener/quote/list"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': "https://xueqiu.com/hq",
    }
    cookies = trans_cookie(settings.env('XUEQIU_COOKIES'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.browser = webdriver.Firefox()

    def closed(self, spider):
        self.browser.close()

    def industry_request(self, industry, ind_code, page, per_page):
        params = {
            'page': page,
            'size': per_page,
            'order': 'desc',
            'order_by': 'percent',
            'exchange': 'CN',
            'market': 'CN',
            'ind_code': ind_code,
            '_': timestamp(time.time()),
        }
        url = "%s?%s" % (self.api, urlencode(params))
        return scrapy.Request(
            url,
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_stocks,
            meta={
                "page": page,
                "per_page": per_page,
                "industry_id": industry.id,
                "ind_code": ind_code
            }
        )

    def parse(self, response):
        # 首先创建 1 级分类
        data = dict(name="申万行业", type=self.type, level=1)
        top_item = IndustryItem(**data)
        first_industry, _ = Industry.objects.get_or_create(**data)
        yield top_item

        # 创建 2 级
        top_sel = response.css('div.nav-container > ul.second-nav > li:nth-child(3)')
        for sel in top_sel.css('ul > li > a'):
            second_item = IndustryItem()
            second_item['parent'] = top_item['name']
            second_item['name'] = sel.xpath('./text()').get()
            second_item['level'] = 2
            second_item['type'] = self.type

            second_industry, _ = Industry.objects.get_or_create(
                name=second_item['name'],
                parent=first_industry,
                type=self.type,
                level=second_item['level']
            )

            yield second_item

            # href = sel.xpath('./@href').get()
            ind_code = sel.xpath('./@data-level2code').get()

            yield self.industry_request(second_industry, ind_code, 1, 30)

    def parse_stocks(self, response):
        body = json.loads(response.body)
        data = body.get('data', {})
        count = int(data.get('count', 0))

        industry_id = response.meta['industry_id']
        page = response.meta['page']
        per_page = response.meta['per_page']
        ind_code = response.meta['ind_code']

        industry = Industry.objects.filter(id=industry_id).first()

        if page * per_page < count:
            yield self.industry_request(industry, ind_code, page + 1, per_page)

        for stock in data.get('list', []):
            item = StockItem()
            item['name'] = stock.get('name')
            item['code'] = stock.get('symbol')

            stock = Stock.objects.filter(code=item['code']).first()

            if industry and stock:
                IndustryStock.objects.get_or_create(
                    stock=stock,
                    industry=industry
                )

            yield item
