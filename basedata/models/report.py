from django.db import models


class ReportType(models.Model):
    REPORT_TYPES = [
        ('primary_indicator', '主要指标'),
        ('profit', '利润表'),
        ('balance', '资产负债表'),
        ('cash_flow', '现金流量表'),
    ]
    name = models.CharField('报告类型', max_length=200)
    slug = models.CharField(max_length=200, null=True)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报告类型'
        verbose_name_plural = verbose_name


class AccountingSubject(models.Model):
    name = models.CharField('科目名称', max_length=200)
    slug = models.CharField(max_length=200, null=True)
    parent = models.ForeignKey('self', verbose_name='上级科目', on_delete=models.CASCADE)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        if self.parent:
            return '%s(%s)' % (self.name, self.parent.name)
        return self.name

    class Meta:
        verbose_name = '会计科目'
        verbose_name_plural = verbose_name


class Report(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    year = models.IntegerField('年度')
    quarter = models.IntegerField('季度')
    is_single_quarter = models.BooleanField('是否单季报', default=True)

    def __str__(self):
        type_quarter = '单季度' if self.is_single_quarter else '报告期'
        return '%s(%s) %s-%s %s(%s)' % (self.stock.name, self.stock.code,
                                        self.year, self.quarter,
                                        self.report_type.name, type_quarter)

    class Meta:
        verbose_name = '报表'
        verbose_name_plural = verbose_name


class ReportItem(models.Model):
    VALUE_TYPES = [
        ('NUMBER', '数字'),
        ('STRING', '字符串'),
    ]
    report = models.ForeignKey(Report, verbose_name='报表', on_delete=models.CASCADE)
    subject = models.ForeignKey(AccountingSubject, on_delete=models.CASCADE)
    value = models.TextField('值', null=True, blank=True)
    value_type = models.CharField('值数据类型', choices=VALUE_TYPES, max_length=64, null=True, blank=True)
    value_unit = models.CharField('数据单位', max_length=64, null=True, blank=True)

    def __str__(self):
        if self.value is not None:
            return '%s: (%s) %s%s' % (self.subject.name, self.value_type, self.value, self.value_unit)
        return self.subject.name

    class Meta:
        verbose_name = '报表项'
        verbose_name_plural = verbose_name
