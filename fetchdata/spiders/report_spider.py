# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode

import scrapy

from basedata.models import Stock
from fetchdata import settings
from fetchdata.items import ReportItem as ScrapyReportItem
from fetchdata.utils import (fromtimestamp, get_params, get_quarter_date,
                             parse_report_name, timestamp, trans_cookie)


class ReportSpider(scrapy.Spider):
    name = 'report_spider'
    allowed_domains = ['xueqiu.com']
    api = "https://stock.xueqiu.com/v5/stock/finance/cn/{report}.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if getattr(self, 'quarter') == 'S0':
            self.is_single_quarter = True
            self.type = 'S0'
        else:
            self.is_single_quarter = False
            self.type = 'all'

        if getattr(self, 'report') == 'income':  # 利润表
            self.report_type = 'consolidated_income_sheet'
        elif getattr(self, 'report') == 'indicator':  # 主要指标
            self.report_type = 'primary_indicator_sheet'
        elif getattr(self, 'report') == 'balance':  # 资产负债表
            self.report_type = 'consolidated_balance_sheet'
        elif getattr(self, 'report') == 'cash_flow':  # 现金流量表
            self.report_type = 'cash_flow_sheet'

    def start_requests(self):
        cookies = trans_cookie(settings.env('XUEQIU_COOKIES'))
        for stock in Stock.objects.only('listing_date', 'name', 'code').all():
            params = {
                "symbol": stock.code,
                "type": self.type,
                "is_detail": True,
                "count": 5,
                "timestamp": "",
            }

            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': settings.env('STOCK_DETAIL_API_REFERER').format(code=stock.code),
            }

            url = "%s?%s" % (self.api.format(report=getattr(self, 'report')), urlencode(params))
            yield scrapy.Request(url, self.parse, cookies=cookies, headers=headers, meta={
                "stock": stock,
            })

    def parse(self, response):
        body = json.loads(response.body)
        data = body.get('data', {})

        for report in data.get('list', []):
            if isinstance(report, dict):
                report_data = report.copy()
                del report_data['report_date']
                del report_data['report_name']

                yield ScrapyReportItem({
                    "stock_id": response.meta['stock'].id,
                    "stock_name": response.meta['stock'].name,
                    "stock_code": response.meta['stock'].code,
                    "report_date": fromtimestamp(report.get('report_date')) if report.get('report_date') else None,
                    "report_name": report.get('report_name', ''),
                    "report_data": report_data,
                    "report_type": self.report_type,
                    "is_single_quarter": self.is_single_quarter,
                    })

        # 上市日期
        listed_date = response.meta['stock'].listing_date
        if listed_date:
            listed_year = listed_date.year
        else:
            listed_year = 2008

        last_report_name = data.get('last_report_name', '')

        last_report_year, last_report_quarter = parse_report_name(last_report_name)
        if last_report_year and last_report_quarter:
            # 默认追踪到上市前两年的报告
            if last_report_year > listed_year - 2:
                params = get_params(response)

                unixtime = timestamp(get_quarter_date(last_report_year - 1, last_report_quarter)) + 1

                params['timestamp'] = unixtime

                url = "%s?%s" % (self.api.format(report=getattr(self, 'report')), urlencode(params))
                yield scrapy.Request(url, self.parse,
                                     cookies=response.request.cookies,
                                     headers=response.request.headers,
                                     meta=response.meta)
