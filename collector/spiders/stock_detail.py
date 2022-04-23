import json
from urllib.parse import urlencode

import scrapy

from basedata.models.stock import Stock
from collector.items import StockItem
from collector.utils import fromtimestamp
from tdxStock.helpers import read_cookie


class StockDetailSpider(scrapy.Spider):
    name = 'stock_detail'
    allowed_domains = ['xueqiu.com']

    cookies = read_cookie("xueqiu")
    api = "https://stock.xueqiu.com/v5/stock/f10/cn/company.json"
    referer = "https://xueqiu.com/snowman/S/{code}/detail"

    def start_requests(self):
        # for stock in Stock.objects.only('name', 'code').all():
        for stock in Stock.objects.filter(company_name__isnull=True).only('name', 'code').all():
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': self.referer.format(code=stock.code),
            }

            params = {"symbol": stock.code}
            url = "%s?%s" % (self.api, urlencode(params))

            yield scrapy.Request(url, cookies=self.cookies,
                                 headers=headers,
                                 meta={"stock_code": stock.code})

    def parse(self, response):
        body = json.loads(response.body)

        company = body.get('data', {}).get('company', {})
        if company:
            item = StockItem()
            item['name'] = company.get('org_short_name_cn')
            item['code'] = response.meta.get('stock_code')
            item['company_name'] = company.get('org_name_cn')
            item['former_name'] = company.get('pre_name_cn')
            item['actual_controller'] = company.get('actual_controller')
            item['ownership_nature'] = company.get('classi_name')
            item['primary_business'] = company.get('main_operation_business')
            item['company_profile'] = company.get('org_cn_introduction')
            item['chairman'] = company.get('chairman')
            item['legal_person'] = company.get('legal_representative')
            item['general_manager'] = company.get('general_manager')
            item['secretary'] = company.get('secretary')
            item['registered_capital'] = company.get('reg_asset')
            item['employees_num'] = company.get('staff_num')
            item['management_num'] = company.get('executives_nums')
            item['distribution_amount'] = company.get('actual_issue_vol')
            item['first_price'] = company.get('issue_price')
            item['raise_money'] = company.get('actual_rc_net_amt')
            item['first_pe'] = company.get('pe_after_issuing')
            item['online_success_rate'] = company.get('online_success_rate_of_issue')
            item['tel'] = company.get('telephone')
            item['zip_code'] = company.get('postcode')
            item['fax'] = company.get('fax')
            item['email'] = company.get('email')
            item['homepage'] = company.get('org_website')
            item['registered_address'] = company.get('reg_address_cn')
            item['office_address'] = company.get('office_address_cn')

            if item['code'].startswith('SH'):
                item['exchange_code'] = 'XSHG'
            elif item['code'].startswith('SZ'):
                item['exchange_code'] = 'XSHE'

            if isinstance(company.get('established_date'), int):
                item['found_date'] = fromtimestamp(company.get('established_date'))

            if isinstance(company.get('listed_date'), int):
                item['listing_date'] = fromtimestamp(company.get('listed_date'))

            yield item
