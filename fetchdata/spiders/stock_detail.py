# -*- coding: utf-8 -*-
import scrapy


class StockDetailSpider(scrapy.Spider):
    name = 'stock_detail'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']

    def parse(self, response):
        pass
