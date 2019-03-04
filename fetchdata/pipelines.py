# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from twisted.internet.defer import ensureDeferred

from basedata.models import (AccountingSubject, Report, ReportItem, ReportType,
                             Stock)
from fetchdata.utils import parse_report_name

from .spiders.report_spider import ReportSpider
from .spiders.stock_detail import StockDetailSpider
from .spiders.stock_list import StockSpider


class StockPipeline(object):
    def __init__(self):
        self.codes = {}
        for stock in Stock.objects.only('code', 'name').all():
            self.codes[stock.code] = stock.name

    def process_item(self, item, spider):
        if isinstance(spider, StockSpider):
            if item['code'] in self.codes:
                if item['name'] == self.codes[item['code']]:
                    # 去重
                    raise DropItem("Duplicate item found: %s" % item)
                else:
                    # 要更新
                    self.codes.update({item['code']: item['name']})
                    Stock.objects.filter(code=item['code']).update(name=item['name'])
                    return item
            else:
                # 新增的
                self.codes.update({item['code']: item['name']})
                Stock.objects.create(**dict(item))
                return item

        elif isinstance(spider, StockDetailSpider):
            del item['name']
            Stock.objects.filter(code=item['code']).update(**dict(item))
            return item

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
        if isinstance(spider, ReportSpider):
            self.download(item)

        # 否则直接返回
        return item

    def download(self, item):
        """异步下载"""
        d = ensureDeferred(self.download_report(item))

        # def success(item):
        #    return item
        # d.addCallback(success)

        return d

    async def download_report(self, item):
        report_year, report_quarter = parse_report_name(item['report_name'])
        if report_year is None or report_quarter is None:
            raise DropItem("无法解析的报告: %s %s" % (item['stock_name'], item['report_name']))

        report_type = self.get_report_type(item['report_type'])
        # 获取报告对象
        report, created = await self.check_report(
            stock_id=item['stock_id'],
            report_type=report_type,
            is_single_quarter=item.get('is_single_quarter'),
            year=report_year,
            quarter=report_quarter,
            report_name=item.get('report_name'),
            report_date=item.get('report_date')
        )

        await self.download_items(report, created, item)

    async def download_items(self, report, created, item):
        if created or not ReportItem.objects.filter(report=report).exists():
            items_to_insert = list()
            for slug, value in item['report_data'].items():
                subject = self.get_subject(report.report_type, slug)

                if isinstance(value, list):
                    value = value[0]

                if isinstance(value, int) or isinstance(value, float):
                    value_type = ReportItem.NUMBER_TYPE
                else:
                    value_type = ReportItem.STRING_TYPE

                items_to_insert.append(ReportItem(
                    report=report,
                    subject=subject,
                    value_number=value if value_type == ReportItem.NUMBER_TYPE else None,
                    value=value if value_type != ReportItem.NUMBER_TYPE else None,
                    value_type=value_type
                ))

            ReportItem.objects.bulk_create(items_to_insert)

    async def check_report(self, stock_id, report_type, is_single_quarter, year, quarter, report_name, report_date):
        """检查是否已经下载, 去重"""
        return Report.objects.get_or_create(
            stock_id=stock_id,
            report_type=report_type,
            is_single_quarter=is_single_quarter,
            year=year,
            quarter=quarter,
            defaults={
                'report_date': report_date,
                'name': report_name,
            }
        )
