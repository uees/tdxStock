# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from basedata.models.stock import Stock
from .spiders.stock_list import StockSpider
from .spiders.stock_detail import StockDetailSpider


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
            Stock.objects.filter(code=item['code']).update(**dict(item))
            return item

        return item
