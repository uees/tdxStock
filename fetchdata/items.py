# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    """股票"""
    name = scrapy.Field()
    code = scrapy.Field()
    exchange_code = scrapy.Field()
    company_name = scrapy.Field()
    former_name = scrapy.Field()
    actual_controller = scrapy.Field()
    ownership_nature = scrapy.Field()
    primary_business = scrapy.Field()
    company_profile = scrapy.Field()
    operating_scope = scrapy.Field()
    chairman = scrapy.Field()
    legal_person = scrapy.Field()
    general_manager = scrapy.Field()
    secretary = scrapy.Field()
    found_date = scrapy.Field()
    registered_capital = scrapy.Field()
    employees_num = scrapy.Field()
    management_num = scrapy.Field()
    listing_date = scrapy.Field()
    distribution_amount = scrapy.Field()
    first_price = scrapy.Field()
    raise_money = scrapy.Field()
    first_pe = scrapy.Field()
    online_success_rate = scrapy.Field()
    tel = scrapy.Field()
    zip_code = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    registered_address = scrapy.Field()
    office_address = scrapy.Field()
    updated_at = scrapy.Field()
    last_report = scrapy.Field()
    territory = scrapy.Field()


class IndustryItem(scrapy.Item):
    """行业"""
    parent = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    type = scrapy.Field()
    memo = scrapy.Field()


class ConceptItem(scrapy.Item):
    """概念"""
    name = scrapy.Field()
    memo = scrapy.Field()


class TerritoryItem(scrapy.Item):
    """地域"""
    name = scrapy.Field()
    memo = scrapy.Field()


class SectionItem(scrapy.Item):
    """版块"""
    name = scrapy.Field()
    memo = scrapy.Field()


class ReportItem(scrapy.Item):
    """报表"""
    stock_id = scrapy.Field()
    stock_name = scrapy.Field()
    stock_code = scrapy.Field()
    report_date = scrapy.Field()
    report_name = scrapy.Field()
    report_data = scrapy.Field()
    report_type = scrapy.Field()
    is_single_quarter = scrapy.Field()
