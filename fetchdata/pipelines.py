# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from twisted.internet import defer, reactor

from basedata.models import (AccountingSubject, Report, ReportItem, ReportType,
                             Stock, XReport, XReportItem)
from fetchdata.utils import parse_report_name, str_fix_null


class StockPipeline(object):
    """下载股票到数据库"""
    def __init__(self):
        self.codes = {}
        for stock in Stock.objects.only('code', 'name').all():
            self.codes[stock.code] = stock.name

    def process_item(self, item, spider):
        if spider.name == "stock_list":
            if item['code'] in self.codes:
                if item['name'] == self.codes[item['code']]:
                    # 去重
                    raise DropItem("Duplicate item found: %s" % item)

                # else 要更新
                self.codes.update({item['code']: item['name']})

                def update_stock():
                    Stock.objects.filter(code=item['code']).update(name=item['name'])

                reactor.callInThread(update_stock)
            else:
                # 新增的
                self.codes.update({item['code']: item['name']})

                def create_stock():
                    Stock.objects.create(**dict(item))

                reactor.callInThread(create_stock)

        elif spider.name == "stock_detail":
            def update_stock():
                del item['name']
                Stock.objects.filter(code=item['code']).update(**dict(item))

            reactor.callInThread(update_stock)

        return item


class IndustryPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "industry_spider" or spider.name == "xueqiu_territory":
            # item is dict(name, code, industry_id)

            # stock = Stock.objects.filter(code__endswith=item['code']).first()

            # if stock and industry:
            #    IndustryStock.objects.get_or_create(
            #        stock=stock,
            #        industry=industry
            #    )
            pass

        return item


class ReportPipeline(object):
    """处理Report的下载"""

    def __init__(self):
        self.report_types = {}
        self.subjects = {}

    def get_report_type(self, slug):
        """优先从缓存获取 report_type"""
        report_type = self.report_types.get(slug)
        if report_type is None:
            report_type = ReportType.objects.get(slug=slug)
            self.report_types[slug] = report_type

        return report_type

    def get_subject(self, report_type, slug):
        """优先从缓存获取 subject"""
        key = "type_%s__%s" % (report_type.id, slug)
        subject = self.subjects.get(key)
        if subject is None:
            subject, _ = AccountingSubject.objects.get_or_create(
                report_type=report_type,
                slug=slug,
                defaults={
                    "memo": "由 spider 创建"
                }
            )
            self.subjects.update({key: subject})

        return subject

    def process_item(self, item, spider):
        # 这个方法必须返回一个 Item (或任何继承类)对象，
        # 或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理
        if spider.name == "report_spider":
            report_name = str_fix_null(item['report_name'])
            report_year, report_quarter = parse_report_name(report_name)
            if report_year is None or report_quarter is None:
                raise DropItem("Reports that cannot be parsed: %s(%s) %s" % (item['stock_name'], item['stock_code'], item['report_name']))

            if item['is_single_quarter']:
                self.reports_model = Report
                self.report_items_model = ReportItem
            else:
                self.reports_model = XReport
                self.report_items_model = XReportItem

            defer.ensureDeferred(self.download_report(item, report_year, report_quarter))

        return item

    async def download_report(self, item, report_year, report_quarter):
        report_type = self.get_report_type(item['report_type'])
        report, created = await self.check_report(
            stock_id=item['stock_id'],
            report_type=report_type,
            year=report_year,
            quarter=report_quarter,
            report_name=item['report_name'],
            report_date=item['report_date']
        )

        await self.download_items(report, created, item)

    async def download_items(self, report, created, item):
        if created or not self.report_items_model.objects.filter(report=report).exists():
            items_to_insert = list()
            for slug, value in item['report_data'].items():
                subject = self.get_subject(report.report_type, slug)

                if isinstance(value, list):
                    value = value[0]

                if isinstance(value, int) or isinstance(value, float):
                    value_type = ReportItem.NUMBER_TYPE
                else:
                    value_type = ReportItem.STRING_TYPE

                items_to_insert.append(self.report_items_model(
                    report=report,
                    subject=subject,
                    value_number=value if value_type == ReportItem.NUMBER_TYPE else None,
                    value=value if value_type != ReportItem.NUMBER_TYPE else None,
                    value_type=value_type
                ))

            self.report_items_model.objects.bulk_create(items_to_insert)

    async def check_report(self, stock_id, report_type, year, quarter, report_name, report_date):
        """检查是否已经下载, 去重"""
        return self.reports_model.objects.get_or_create(
            stock_id=stock_id,
            report_type=report_type,
            year=year,
            quarter=quarter,
            defaults={
                'report_date': report_date,
                'name': report_name,
            }
        )
