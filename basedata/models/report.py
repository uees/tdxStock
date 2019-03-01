from django.db import models


class ReportType(models.Model):
    REPORT_TYPES = [
        ('primary_indicator_sheet', '主要指标'),
        ('consolidated_income_sheet', '利润表'),
        ('consolidated_balance_sheet', '资产负债表'),
        ('cash_flow_sheet', '现金流量表'),
    ]
    parent = models.ForeignKey('self', verbose_name='上级类型', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('报表类型', max_length=200)
    slug = models.CharField(max_length=200, null=True)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_subject_set(self):
        if self.accountingsubject_set.exists():
            return self.accountingsubject_set

        return self.parent.get_subject_set()

    class Meta:
        verbose_name = '报表类型'
        verbose_name_plural = verbose_name


class AccountingSubject(models.Model):
    report_type = models.ForeignKey(ReportType, verbose_name="报表类型", on_delete=models.CASCADE, null=True)
    name = models.CharField('科目名称', max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name='上级科目', on_delete=models.CASCADE, null=True, blank=True)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return "%s -> %s" % (self.report_type.name, self.name)

    class Meta:
        verbose_name = '会计科目'
        verbose_name_plural = verbose_name
        unique_together = ["slug", "report_type"]


class Report(models.Model):
    name = models.CharField('名称', max_length=128, null=True, blank=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    year = models.IntegerField('年度')
    quarter = models.IntegerField('季度')
    report_date = models.DateField('公布日期', null=True, blank=True)
    is_single_quarter = models.BooleanField('是否单季报', default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        type_quarter = '单季度' if self.is_single_quarter else '报告期'
        self.name = '%s(%s) %s-%s %s(%s)' % (self.stock.name, self.stock.code,
                                             self.year, self.quarter,
                                             self.report_type.name, type_quarter)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报表'
        verbose_name_plural = verbose_name
        unique_together = ["stock", "report_type", 'year', 'quarter']


class ReportItem(models.Model):
    VALUE_TYPES = [
        ('NUMBER', '数字'),
        ('STRING', '字符串'),
    ]
    report = models.ForeignKey(Report, verbose_name='报表', on_delete=models.CASCADE)
    subject = models.ForeignKey(AccountingSubject, on_delete=models.CASCADE)
    value = models.CharField('值', max_length=250, null=True, blank=True)
    value_type = models.CharField('值数据类型', choices=VALUE_TYPES, max_length=64, null=True, blank=True)
    value_unit = models.CharField('数据单位', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = '报表项'
        verbose_name_plural = verbose_name
        unique_together = ["report", "subject"]
