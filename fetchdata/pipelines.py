# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.exceptions import DropItem

from basedata.models import Stock, ReportType, Report, AccountingSubject, ReportItem
from fetchdata.utils import parse_report_name

from .spiders.stock_detail import StockDetailSpider
from .spiders.stock_list import StockSpider
from .spiders.report_spider import ReportSpider


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

    def __init__(self, redis_host, redis_port, redis_db):
        # todo 加载并用 redis 缓存各种 ID slug (ReportType, AccountingSubject)
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST', '127.0.0.1'),
            redis_port=crawler.settings.get('REDIS_PORT', 6379),
            redis_db=crawler.settings.get('REDIS_SPIDER_DB', 0)
        )

    def open_spider(self, spider):
        self.pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        self.r = redis.Redis(connection_pool=self.pool)

    def close_spider(self, spider):
        self.r.connection_pool.disconnect()

    def process_item(self, item, spider):
        # 这个方法必须返回一个 Item (或任何继承类)对象，
        # 或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理
        if isinstance(spider, ReportSpider):
            self.download_report(item.copy())
            return item

        # 否则直接返回
        return item

    def download_report(self, item):
        report_year, report_quarter = parse_report_name(item['report_name'])
        if report_year is None or report_quarter is None:
            raise DropItem("无法解析的报告: %s %s" % (item['stock_name'], item['report_name']))

        report_type_id = self.get_report_type_id(item['report_type'])
        # 获取报告对象
        report_id, report_created = self.check_report(
            stock_id=item['stock_id'],
            report_type_id=report_type_id,
            is_single_quarter=item.get('is_single_quarter'),
            year=report_year,
            quarter=report_quarter,
            report_name=item.get('report_name'),
            report_date=item.get('report_date')
        )

        if report_created or not ReportItem.objects.filter(report_id=report_id).exists():
            items_to_insert = list()
            for slug, value in item['report_data'].items():
                subject_id = self.get_subject_id(report_type_id, slug)
                # 创建报告项目
                if isinstance(value, list):
                    value = value[0]

                if isinstance(value, int) or isinstance(value, float):
                    value_type = 'NUMBER'
                else:
                    value_type = 'STRING'

                items_to_insert.append(ReportItem(
                    report_id=report_id,
                    subject_id=subject_id,
                    value=value,
                    value_type=value_type
                ))

            ReportItem.objects.bulk_create(items_to_insert)

    def check_report(self, stock_id, report_type_id, is_single_quarter, year, quarter, report_name, report_date):
        """检查是否已经下载, 去重"""
        name = "basedata.report"
        key = "stock_%s__type_%s__%s_%s__single_%s" % (stock_id, report_type_id, year, quarter, is_single_quarter)
        created = False
        if self.r.hexists(name, key):
            return self.r.hget(name, key), created

        # 获取报告对象
        report, created = Report.objects.get_or_create(
            stock_id=stock_id,
            report_type_id=report_type_id,
            is_single_quarter=is_single_quarter,
            year=year,
            quarter=quarter,
            defaults={
                'report_date': report_date,
                'name': report_name,
            }
        )
        self.r.hset(name, key, report.id)

        return report.id, created

    def get_report_type_id(self, slug):
        """缓存获取 report_type_id"""
        name = "basedata.report_type"
        id = self.r.hget(name, slug)
        if not id:
            report_type = ReportType.objects.get(slug=slug)
            id = report_type.id
            self.r.hset(name, slug, id)

        return id

    def get_subject_id(self, report_type_id, slug):
        """缓存获取 subject_i"""
        name = "basedata.accounting_subject"
        key = "type_%s__%s" % (report_type_id, slug)
        id = self.r.hget(name, key)
        if not id:
            subject, _ = AccountingSubject.objects.get_or_create(
                slug=slug,
                report_type_id=report_type_id,
                defaults={
                    "memo": "由 spider 创建"
                }
            )
            id = subject.id

            self.r.hset(name, key, id)

        return id
