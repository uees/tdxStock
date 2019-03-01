# -*- coding: utf-8 -*-
import json
import re
import sys
from urllib.parse import urlencode

import scrapy

from basedata.models import (AccountingSubject, Report, ReportItem, ReportType,
                             Stock)
from fetchdata import settings
from fetchdata.items import ReportItem as ScrapyReportItem
from fetchdata.utils import (get_params, get_quarter_by_report_type,
                             get_quarter_date, timestamp, trans_cookie, fromtimestamp)


class PrimaryIndicatorSpider(scrapy.Spider):
    name = 'report_spider'
    allowed_domains = ['xueqiu.com']
    api = "https://stock.xueqiu.com/v5/stock/finance/cn/{report}.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if getattr(self, 'quarter', 'S0') == 'S0':
            self.is_single_quarter = True
        else:
            self.is_single_quarter = False

        if getattr(self, 'report') == 'income':  # 利润表
            self.report_type = ReportType.objects.get(slug='consolidated_income_sheet')
            self.quarter_report_type = ReportType.objects.get(slug='quarter_consolidated_income_sheet')
        elif getattr(self, 'report') == 'indicator':  # 主要指标
            self.report_type = ReportType.objects.get(slug='primary_indicator_sheet')
            self.quarter_report_type = ReportType.objects.get(slug='quarter_primary_indicator_sheet')
        elif getattr(self, 'report') == 'balance':  # 资产负债表
            self.report_type = ReportType.objects.get(slug='consolidated_balance_sheet')
            self.quarter_report_type = ReportType.objects.get(slug='quarter_consolidated_balance_sheet')
        elif getattr(self, 'report') == 'cash_flow':  # 现金流量表
            self.report_type = ReportType.objects.get(slug='cash_flow_sheet')
            self.quarter_report_type = ReportType.objects.get(slug='quarter_cash_flow_sheet')
        else:
            raise Exception('没有指定 report 参数')
            sys.exit()

    def start_requests(self):
        cookies = trans_cookie(settings.env('XUEQIU_COOKIES'))
        for stock in Stock.objects.only('listing_date', 'name', 'code').all():
            params = {
                "symbol": stock.code,
                "type": getattr(self, 'quarter', 'all'),
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

        p = re.compile(r'(?P<year>\d{4})(?P<report_type>.+)')
        reports = data.get('list', [])

        for report in reports:
            if isinstance(report, dict):
                report_type = self.quarter_report_type if self.is_single_quarter else self.report_type

                report_name = report.get('report_name', '')
                match = p.match(report_name)
                if match:
                    report_year = int(match.group('year'))
                    report_quarter = get_quarter_by_report_type(match.group('report_type'))

                    report_date = report.get('report_date')
                    defaults = {}
                    if report_date:
                        defaults.update({
                            'report_date': fromtimestamp(report_date)
                        })

                    # 获取报告对象
                    report_obj, _ = Report.objects.update_or_create(
                        name=report.get('report_name'),
                        stock=response.meta['stock'],
                        report_type=report_type,
                        year=report_year,
                        quarter=report_quarter,
                        is_single_quarter=self.is_single_quarter,
                        defaults=defaults
                    )

                    for slug, value in report.items():
                        # 获得 subject
                        subject, _ = AccountingSubject.objects.get_or_create(
                            slug=slug,
                            report_type=self.report_type,
                            defaults={
                                "memo": "由 spider 创建"
                            }
                        )

                        # 创建报告项目
                        if isinstance(value, list):
                            value = value[0]

                        if isinstance(value, int) or isinstance(value, float):
                            value_type = 'NUMBER'
                        else:
                            value_type = 'STRING'

                        report_item, _ = ReportItem.objects.update_or_create(
                            report=report_obj,
                            subject=subject,
                            defaults={
                                'value': value,
                                'value_type': value_type,
                            }
                        )

                    yield ScrapyReportItem({
                        "report_date": report.get('report_date'),
                        "report_name": report.get('report_name')
                    })

        # 上市日期
        listed_date = response.meta['stock'].listing_date
        if listed_date:
            listed_year = listed_date.year
        else:
            listed_year = 2008

        last_report_name = data.get('last_report_name', '')
        match = p.match(last_report_name)
        if match:
            last_report_year = int(match.group('year'))
            last_report_quarter = get_quarter_by_report_type(match.group('report_type'))

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
