from scrapy.exceptions import DropItem
from twisted.internet import defer, reactor

from basedata.models import (AccountingSubject, Concept, ConceptStock,
                             Industry, IndustryStock, Report, ReportItem,
                             ReportType, Stock, Territory, XReport,
                             XReportItem)
from tdxStock.abstract_models import DynamicModel


class StockPipeline(object):
    """下载股票到数据库"""

    def __init__(self):
        self.stock_map = {}
        for stock in Stock.objects.only('code', 'name').all():
            self.stock_map[stock.code] = stock.name

    def process_item(self, item, spider):
        if spider.name == "stock_list":
            if item['code'] in self.stock_map:
                if item['name'] == self.stock_map[item['code']]:
                    # 去重
                    raise DropItem("Duplicate item found: %s" % item)

                # else 要更新
                self.stock_map.update({item['code']: item['name']})

                def update_stock():
                    Stock.objects.filter(code=item['code']).update(name=item['name'], pinyin=item["pinyin"])

                reactor.callInThread(update_stock)
            else:
                # 新增的
                self.stock_map.update({item['code']: item['name']})

                def create_stock():
                    Stock.objects.create(**dict(item))

                reactor.callInThread(create_stock)

        elif spider.name == "stock_detail":
            def update_stock():
                del item['name']
                Stock.objects.filter(code=item['code']).update(**dict(item))

            reactor.callInThread(update_stock)

        else:
            return item


class IndustryPipeline(object):

    def process_item(self, item, spider):
        if spider.name in ("industry_zjh", "industry_sw"):
            # item is dict(name, code, industry_id)
            async def process_industry_stock():
                industry = Industry.objects.filter(pk=item['industry_id']).first()
                stock = Stock.objects.filter(code__endswith=item['code']).first()
                if stock and industry:
                    IndustryStock.objects.get_or_create(
                        stock=stock,
                        industry=industry
                    )

            defer.ensureDeferred(process_industry_stock())
        else:
            return item


class ConceptPipeline(object):

    def process_item(self, item, spider):
        if spider.name in ("concept",):
            # item is dict(name, code, concept_id)
            async def process_concept_stock():
                concept = Concept.objects.filter(pk=item['concept_id']).first()
                stock = Stock.objects.filter(code__endswith=item['code']).first()
                if stock and concept:
                    ConceptStock.objects.get_or_create(
                        stock=stock,
                        concept=concept
                    )

            defer.ensureDeferred(process_concept_stock())
        else:
            return item


class TerritoryPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "territory":
            # item is dict(name, code, territory_id)
            async def process_territory_stock():
                territory = Territory.objects.filter(pk=item['territory_id']).first()
                if territory:
                    Stock.objects.filter(code__endswith=item['code']).update(
                        territory=territory
                    )

            defer.ensureDeferred(process_territory_stock())
        else:
            return item


class ReportPipeline(object):
    """处理Report的下载"""

    def __init__(self):
        self.report_types = {}
        self.subjects = {}

    def process_item(self, item, spider):
        if spider.name == "report":
            defer.ensureDeferred(self.download_report(item))
        else:
            return item

    async def get_report_type(self, slug):
        """优先从缓存获取 report_type"""
        report_type = self.report_types.get(slug)
        if report_type is None:
            report_type = ReportType.objects.get(slug=slug)
            self.report_types[slug] = report_type

        return report_type

    async def get_subject(self, report_type, slug):
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

    async def download_report(self, item):
        report_model = Report if item['is_single_quarter'] else XReport
        report_type = await self.get_report_type(item['report_type'])
        report, created = await self.get_or_create_report(
            report_model,
            stock_id=item['stock_id'],
            report_type=report_type,
            year=item['report_year'],
            quarter=item['report_quarter'],
            defaults={
                'report_date': item['report_date'],
                'name': item['report_name'],
            }
        )

        await self.download_report_items(report, created, item)

    async def download_report_items(self, report, created, item):
        if item['is_single_quarter']:
            report_item_model = DynamicModel(ReportItem, item['report_year'])
        else:
            report_item_model = DynamicModel(XReportItem, item['report_year'])

        async def has_items():
            return report_item_model.objects.filter(report=report).exists()

        if created or not await has_items():
            items_to_insert = list()
            for slug, value in item['report_data'].items():
                subject = await self.get_subject(report.report_type, slug)

                if isinstance(value, list):
                    value = value[0]

                if isinstance(value, int) or isinstance(value, float):
                    value_type = ReportItem.NUMBER_TYPE
                else:
                    value_type = ReportItem.STRING_TYPE

                items_to_insert.append(report_item_model(
                    report=report,
                    subject=subject,
                    value_number=value if value_type == ReportItem.NUMBER_TYPE else None,
                    value=value if value_type != ReportItem.NUMBER_TYPE else None,
                    value_type=value_type
                ))

            await self.bulk_create_items(report_item_model, items_to_insert)

        elif item['crawl_mode'] == 'all':
            for slug, value in item['report_data'].items():
                subject = await self.get_subject(report.report_type, slug)

                if isinstance(value, list):
                    value = value[0]

                if isinstance(value, int) or isinstance(value, float):
                    value_type = ReportItem.NUMBER_TYPE
                else:
                    value_type = ReportItem.STRING_TYPE

                await self.update_or_create_item(
                    report_item_model,
                    report=report,
                    subject=subject,
                    defaults={
                        "value_number": value if value_type == ReportItem.NUMBER_TYPE else None,
                        "value": value if value_type != ReportItem.NUMBER_TYPE else None,
                        "value_type": value_type,
                    },
                )

    async def get_or_create_report(self, report_model, *args, **kwargs):
        """检查是否已经下载, 去重"""
        return report_model.objects.get_or_create(*args, **kwargs)

    async def update_or_create_item(self, item_model, *args, **kwargs):
        """异步更新报表项"""
        return item_model.objects.update_or_create(*args, **kwargs)

    async def bulk_create_items(self, item_model, items_to_insert):
        """批量插入"""
        return item_model.objects.bulk_create(items_to_insert)
