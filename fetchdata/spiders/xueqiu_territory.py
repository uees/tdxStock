# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver


class XueqiuTerritorySpider(scrapy.Spider):
    name = 'xueqiu_territory'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/hq']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.browser = webdriver.Firefox()

    def closed(self, spider):
        self.browser.close()

    def parse(self, response):
        top_sel = response.css('div.nav-container > ul.second-nav > li:nth-child(3)')
        for sel in top_sel.css('ul > li > a'):
            territory_name = sel.xpath('./text()').get()

            href = sel.xpath('./@href').get()
            level2code = sel.xpath('./@data-level2code').get()

