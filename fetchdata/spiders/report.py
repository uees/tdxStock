import datetime
import json
from urllib.parse import urlencode

import scrapy
from django.db.models import Max

from basedata.models import Report, Stock, XReport
from fetchdata import settings
from fetchdata.items import ReportItem
from fetchdata.utils import (fromtimestamp, get_quarter_date,
                             parse_report_name, str_fix_null, timestamp,
                             trans_cookie)


class ReportSpider(scrapy.Spider):
    name = 'report'
    allowed_domains = ['xueqiu.com']
    api = "https://stock.xueqiu.com/v5/stock/finance/cn/{report}.json"
    referer = "https://xueqiu.com/snowman/S/{code}/detail"
    cookies = trans_cookie(settings.env('XUEQIU_COOKIES'))

    def __init__(self, quarter, report, crawl_mode, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.quarter = quarter
        self.report = report
        self.crawl_mode = crawl_mode  # all or append, 全量或追加

        # 单季参数  S0 S1 S2 S3 S4
        # 报告期参数  all Q1 Q2 Q3 Q4
        if self.quarter == 'S0':
            self.is_single_quarter = True
            self.type = 'S0'
        else:
            self.is_single_quarter = False
            self.type = 'all'

        if self.report == 'income':  # 利润表
            self.report_type = 'consolidated_income_sheet'
        elif self.report == 'indicator':  # 主要指标
            self.report_type = 'primary_indicator_sheet'
        elif self.report == 'balance':  # 资产负债表
            self.report_type = 'consolidated_balance_sheet'
        elif self.report == 'cash_flow':  # 现金流量表
            self.report_type = 'cash_flow_sheet'

        self.api = self.api.format(report=self.report)

    def closed(self, spider):
        # 关闭时更新最后报表日期
        if self.is_single_quarter:
            stocks = Report.objects.values('stock_id').annotate(last_date=Max('report_date'))
            for stock in stocks:
                Stock.objects.filter(pk=stock['stock_id']).update(last_report_date=stock['last_date'])
        else:
            stocks = XReport.objects.values('stock_id').annotate(last_date=Max('report_date'))
            for stock in stocks:
                Stock.objects.filter(pk=stock['stock_id']).update(last_all_report_date=stock['last_date'])

    def start_requests(self):
        # 获取报表数<=4的股票
        # if self.is_single_quarter:
        #    qs = Stock.objects.annotate(
        #        reports_num=Count('report', filter=Q(report__report_type__slug=self.report_type))
        #    )
        # else:
        #    qs = Stock.objects.annotate(
        #        reports_num=Count('xreport', filter=Q(xreport__report_type__slug=self.report_type))
        #    )

        # stocks = qs.filter(reports_num__lte=4).all()

        stocks = Stock.objects.all()

        for stock in stocks:
            yield self.make_request(stock)

    def make_request(self, stock, timestamp=''):
        params = {
            "symbol": stock.code,
            "type": self.type,  # S0 or all
            "is_detail": True,
            "count": 5,
            "timestamp": timestamp,
        }

        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.referer.format(code=stock.code),
        }

        url = "%s?%s" % (self.api, urlencode(params))
        return scrapy.Request(
            url,
            callback=self.parse,
            cookies=self.cookies,
            headers=headers,
            meta={"stock": stock}
        )

    def parse(self, response):
        body = json.loads(response.body)
        data = body.get('data', {})

        last_report_name = data.get('last_report_name')  # 当前请求中的最后报告名
        if not last_report_name:
            # 已经无报表了
            return

        stock = response.meta['stock']
        first_report_date = self.get_first_report_date(stock)

        last_report_year, last_report_quarter = parse_report_name(last_report_name)
        if last_report_year and last_report_quarter:
            if last_report_year > first_report_date.year:
                # 雪球根据 timestamp 分页
                unixtime = timestamp(get_quarter_date(last_report_year - 1, last_report_quarter)) + 1
                yield self.make_request(stock, unixtime)

        for report in data.get('list', []):
            if isinstance(report, dict):
                report_date = fromtimestamp(report.get('report_date')) if report.get('report_date') else None
                report_name = str_fix_null(report.get('report_name', ''))
                report_year, report_quarter = parse_report_name(report_name)

                # 有效的报表可以被 parse_report_name 解析
                if report_year and report_quarter:
                    report_data = report.copy()
                    del report_data['report_date']
                    del report_data['report_name']

                    yield ReportItem({
                        "stock_id": stock.id,
                        "stock_name": stock.name,
                        "stock_code": stock.code,
                        "report_date": report_date,
                        "report_name": report_name,
                        "report_data": report_data,
                        "report_type": self.report_type,
                        "report_year": report_year,
                        "report_quarter": report_quarter,
                        "is_single_quarter": self.is_single_quarter,
                        "crawl_mode": self.crawl_mode,
                    })

    def get_first_report_date(self, stock: Stock):
        first_report_date = None
        if self.crawl_mode == 'append':
            first_report_date = stock.last_report_date if self.is_single_quarter \
                else stock.last_all_report_date

        if first_report_date is None:
            # 上市日期
            if stock.listing_date:
                first_report_date = stock.listing_date - datetime.timedelta(days=365) * 2
            else:
                first_report_date = datetime.date(1997, 1, 1)

        return first_report_date
