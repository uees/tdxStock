from django.db import models


class ReportType(models.Model):
    REPORT_TYPES = [
        ('primary_indicator_sheet', '主要指标'),
        ('consolidated_income_sheet', '利润表'),
        ('consolidated_balance_sheet', '资产负债表'),
        ('cash_flow_sheet', '现金流量表'),
    ]
    name = models.CharField('报表类型', max_length=200)
    slug = models.CharField(max_length=200, null=True, unique=True)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报表'
        verbose_name_plural = verbose_name
        unique_together = ["stock", "report_type", 'is_single_quarter', 'year', 'quarter']


class ReportItem(models.Model):
    """
    报表项目
    这个表中数据是千万级以上的, 能用数值存储尽量用数值类型
    """
    VALUE_TYPES = [
        (1, '数值'),
        (2, '字符串'),
    ]
    UNIT_TYPES = [
        (1, '元'),
        (2, '万元'),
        (3, '亿'),
        (4, '个'),
        (5, '人'),
        (6, '次'),
        (7, '%'),
    ]
    report = models.ForeignKey(Report, verbose_name='报表', on_delete=models.CASCADE, db_index=True)
    subject = models.ForeignKey(AccountingSubject, on_delete=models.CASCADE)
    value_number = models.DecimalField('数值', max_digits=30, decimal_places=4, null=True, blank=True)
    value = models.CharField('值', max_length=64, null=True, blank=True)
    value_type = models.SmallIntegerField('值类型', choices=VALUE_TYPES, null=True, blank=True)
    value_unit = models.SmallIntegerField('值单位', choices=UNIT_TYPES, null=True, blank=True)

    def __str__(self):
        return self.subject.name

    def get_value(self):
        if self.value_type == 1:
            return self.value_number, self.value_type

        return self.value, self.value_type

    class Meta:
        verbose_name = '报表项'
        verbose_name_plural = verbose_name
