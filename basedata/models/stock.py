from django.db import models

from tdxStock.fields import UnsignedAutoField


class Stock(models.Model):
    """股票"""
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField('名称', max_length=64, db_index=True)
    code = models.CharField('代码', max_length=32, unique=True)
    exchange_code = models.CharField('交易市场', max_length=32, null=True, blank=True)  # 交易市场, 例如，XSHG-上海证券交易所；XSHE-深圳证券交易所
    company_name = models.CharField('公司名称', max_length=200, null=True, blank=True)
    former_name = models.CharField('曾用名', max_length=200, null=True, blank=True)
    actual_controller = models.CharField('实际控制人', max_length=200, null=True, blank=True)
    ownership_nature = models.CharField('所有制性质名称', max_length=200, null=True, blank=True)
    primary_business = models.TextField('主营业务', null=True, blank=True)
    company_profile = models.TextField('公司简介', null=True, blank=True)
    operating_scope = models.TextField('经营范围', null=True, blank=True)
    chairman = models.CharField('董事长', max_length=64, null=True, blank=True)
    legal_person = models.CharField('法人代表', max_length=64, null=True, blank=True)
    general_manager = models.CharField('总经理', max_length=64, null=True, blank=True)
    secretary = models.CharField('董秘', max_length=64, null=True, blank=True)
    found_date = models.DateField('成立日期', null=True, blank=True)
    registered_capital = models.DecimalField('注册资本(元)', max_digits=20, decimal_places=2, null=True, blank=True)
    employees_num = models.IntegerField('员工人数', null=True, blank=True)
    management_num = models.IntegerField('管理层人数', null=True, blank=True)
    listing_date = models.DateField('上市日期', null=True, blank=True)
    distribution_amount = models.BigIntegerField('发行量', null=True, blank=True)
    first_price = models.FloatField('发行价格', null=True, blank=True)
    raise_money = models.DecimalField('募集资金', max_digits=20, decimal_places=2, null=True, blank=True)
    first_pe = models.FloatField('发行市盈率', null=True, blank=True)
    online_success_rate = models.FloatField('网上中签率', null=True, blank=True)
    tel = models.CharField('联系电话', max_length=200, null=True, blank=True)
    zip_code = models.CharField('邮政编码', max_length=64, null=True, blank=True)
    fax = models.CharField('传真', max_length=200, null=True, blank=True)
    email = models.CharField('电子邮箱', max_length=250, null=True, blank=True)
    homepage = models.CharField('公司网址', max_length=250, null=True, blank=True)
    registered_address = models.CharField('注册地址', max_length=250, null=True, blank=True)
    office_address = models.CharField('办公地址', max_length=250, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, editable=False)
    last_report_date = models.DateField('最后报告日期（单单季）', null=True, blank=True, editable=False)
    last_all_report_date = models.DateField('最后报告日期（报告期）', null=True, blank=True, editable=False)

    territory = models.ForeignKey('Territory', verbose_name='地域', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '股票'
        verbose_name_plural = verbose_name
