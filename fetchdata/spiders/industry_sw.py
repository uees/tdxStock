import json
import time
from urllib.parse import urlencode

import scrapy
from selenium import webdriver

from basedata.models import Industry
from fetchdata.utils import get_params, timestamp
from tdxStock.helpers import read_cookie


class SWIndustrySpider(scrapy.Spider):
    name = 'industry_sw'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/hq']
    type = "申万行业分类"
    api = "https://xueqiu.com/service/v5/stock/screener/quote/list"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': "https://xueqiu.com/hq",
    }
    cookies = read_cookie("xueqiu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.browser = webdriver.Firefox()

    def closed(self, spider):
        self.browser.close()

    def stock_list_request(self, industry_id, params):
        url = "%s?%s" % (self.api, urlencode(params))
        return scrapy.Request(
            url,
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_stocks,
            meta={
                "industry_id": industry_id,
            }
        )

    def parse(self, response):
        # 首先创建 1 级分类
        data = dict(name="申万行业", type=self.type, level=1)
        # 行业表数据的创建会阻塞，因数据量少可以接受阻塞
        first_industry, _ = Industry.objects.get_or_create(**data)

        # 创建 2 级分类
        top_sel = response.css('div.nav-container > ul.second-nav > li:nth-child(3)')
        for sel in top_sel.css('ul > li > a'):
            second_industry, _ = Industry.objects.get_or_create(
                name=sel.xpath('./text()').get(),
                parent=first_industry,
                type=self.type,
                level=2
            )

            # href = sel.xpath('./@href').get()
            ind_code = sel.xpath('./@data-level2code').get()

            params = {
                'page': 1,
                'size': 30,
                'order': 'desc',
                'order_by': 'percent',
                'exchange': 'CN',
                'market': 'CN',
                'ind_code': ind_code,
                '_': timestamp(time.time()),
            }

            yield self.stock_list_request(second_industry.id, params)

    def parse_stocks(self, response):
        body = json.loads(response.body)
        data = body.get('data', {})
        count = int(data.get('count', 0))

        industry_id = response.meta['industry_id']

        params = get_params(response)
        page = int(params['page'])
        per_page = int(params['size'])

        if page * per_page < count:
            params.update({"page": page + 1})
            yield self.stock_list_request(industry_id, params)

        for stock in data.get('list', []):
            yield dict(
                name=stock.get('name'),
                code=stock.get('symbol'),
                industry_id=industry_id
            )
