from django.db import models


class Stock(models.Model):
    """股票"""
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)
    company_name = models.CharField(max_length=200)  # 公司名称
    former_name = models.CharField(max_length=200)  # 曾用名
    actual_controller = models.CharField(max_length=200)  # 实际控制人
    ownership_nature = models.CharField(max_length=200)  # 所有制性质名称
    primary_business = models.TextField()  # 主营业务
    company_profile = models.TextField()  # 公司简介
    chairman = models.CharField(max_length=64)  # 董事长
    legal_person = models.CharField(max_length=64)  # 法人代表
    general_manager = models.CharField(max_length=64)  # 总经理
    secretary = models.CharField(max_length=64)  # 董秘
    found_date = models.DateField()  # 成立日期
    registered_capital = models.DecimalField()  # 注册资本(元)
    employees_num = models.IntegerField()  # 员工人数
    management_num = models.IntegerField()  # 管理层人数
    listing_date = models.DecimalField()  # 上市日期
    distribution_amount = models.BigIntegerField()  # 发行量
    first_price = models.FloatField()  # 发行价格
    raise_money = models.DecimalField()  # 募集资金
    first_pe = models.FloatField()  # 发行市盈率
    online_success_rate = models.FloatField()  # 网上中签率
    tel =  models.CharField(max_length=200)  # 联系电话
    zip_code = models.CharField(max_length=64)  # 邮政编码
    fax = models.CharField(max_length=200)  # 传真
    email = models.CharField(max_length=250)  # 电子邮箱
    homepage = models.CharField(max_length=250)  # 公司网址
    registered_address = models.CharField(max_length=250)  # 注册地址
    office_address = models.CharField(max_length=250)  # 办公地址
