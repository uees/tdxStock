from django.db import models


class Stock(models.Model):
    """股票"""
    name = models.CharField('名称', max_length=64)
    code = models.CharField('代码', max_length=32)
    exchange_code = models.CharField('交易市场', max_length=32)  # 交易市场, 例如，XSHG-上海证券交易所；XSHE-深圳证券交易所
    company_name = models.CharField('公司名称', max_length=200)  # 公司名称
    former_name = models.CharField('曾用名', max_length=200)  # 曾用名
    actual_controller = models.CharField('实际控制人', max_length=200)  # 实际控制人
    ownership_nature = models.CharField('所有制性质名称', max_length=200)  # 所有制性质名称
    primary_business = models.TextField('主营业务')  # 主营业务
    company_profile = models.TextField('公司简介')  # 公司简介
    chairman = models.CharField('董事长', max_length=64)  # 董事长
    legal_person = models.CharField('法人代表', max_length=64)  # 法人代表
    general_manager = models.CharField('总经理', max_length=64)  # 总经理
    secretary = models.CharField('董秘', max_length=64)  # 董秘
    found_date = models.DateField('成立日期')  # 成立日期
    registered_capital = models.DecimalField('注册资本(元)', max_digits=20, decimal_places=2)  # 注册资本(元)
    employees_num = models.IntegerField('员工人数')  # 员工人数
    management_num = models.IntegerField('管理层人数')  # 管理层人数
    listing_date = models.DateField('上市日期')  # 上市日期
    distribution_amount = models.BigIntegerField('发行量')  # 发行量
    first_price = models.FloatField('发行价格')  # 发行价格
    raise_money = models.DecimalField('募集资金', max_digits=20, decimal_places=2)  # 募集资金
    first_pe = models.FloatField('发行市盈率')  # 发行市盈率
    online_success_rate = models.FloatField('网上中签率')  # 网上中签率
    tel = models.CharField('联系电话', max_length=200)  # 联系电话
    zip_code = models.CharField('邮政编码', max_length=64)  # 邮政编码
    fax = models.CharField('传真', max_length=200)  # 传真
    email = models.CharField('电子邮箱', max_length=250)  # 电子邮箱
    homepage = models.CharField('公司网址', max_length=250)  # 公司网址
    registered_address = models.CharField('注册地址', max_length=250)  # 注册地址
    office_address = models.CharField('办公地址', max_length=250)  # 办公地址

    territory = models.ForeignKey('Territory', verbose_name='地域', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s(%s)" % (self.name, self.code)

    class Meta:
        verbose_name = '股票'
        verbose_name_plural = verbose_name
