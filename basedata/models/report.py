from django.db import models

from tdxStock.fields import UnsignedAutoField, UnsignedBigAutoField


class ReportType(models.Model):
    """报表类型"""
    REPORT_TYPES = [
        ('primary_indicator_sheet', '主要指标'),
        ('consolidated_income_sheet', '利润表'),
        ('consolidated_balance_sheet', '资产负债表'),
        ('cash_flow_sheet', '现金流量表'),
    ]

    id = UnsignedAutoField(primary_key=True)
    name = models.CharField('报表类型', max_length=200)
    slug = models.CharField(max_length=200, null=True, unique=True)
    memo = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报表类型'
        verbose_name_plural = verbose_name


class AccountingSubject(models.Model):
    """会计科目"""
    id = UnsignedAutoField(primary_key=True)
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
    """单季报表"""
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField('名称', max_length=128, null=True, blank=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    year = models.IntegerField('年度')
    quarter = models.IntegerField('季度')
    report_date = models.DateField('公布日期', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '单季度报表'
        verbose_name_plural = verbose_name
        unique_together = ["stock", "report_type", 'year', 'quarter']


class ReportItem(models.Model):
    # todo 分表
    """
    单季报表项目
    这个表中数据是千万级以上的, 能用数值存储尽量用数值类型
    """
    NUMBER_TYPE = 1
    STRING_TYPE = 2

    VALUE_TYPES = [
        (NUMBER_TYPE, '数值'),
        (STRING_TYPE, '字符串'),
    ]

    YUAN = 1
    WAN_YUAN = 2
    YI = 3
    GE = 4
    REN = 5
    CI = 6
    RATE = 7

    UNIT_TYPES = [
        (YUAN, '元'),
        (WAN_YUAN, '万元'),
        (YI, '亿'),
        (GE, '个'),
        (REN, '人'),
        (CI, '次'),
        (RATE, '%'),
    ]

    id = UnsignedBigAutoField(primary_key=True)
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
        verbose_name = '单季度报表项目'
        verbose_name_plural = verbose_name


class XReport(models.Model):
    """报告期报表"""
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField('名称', max_length=128, null=True, blank=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    year = models.IntegerField('年度')
    quarter = models.IntegerField('季度')
    report_date = models.DateField('公布日期', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '报告期报表'
        verbose_name_plural = verbose_name
        unique_together = ["stock", "report_type", 'year', 'quarter']


class XReportItem(models.Model):
    """
    报告期报表项目
    这个表中数据是千万级以上的, 能用数值存储尽量用数值类型
    """

    id = UnsignedBigAutoField(primary_key=True)
    report = models.ForeignKey(XReport, verbose_name='报表', on_delete=models.CASCADE, db_index=True)
    subject = models.ForeignKey(AccountingSubject, on_delete=models.CASCADE)
    value_number = models.DecimalField('数值', max_digits=30, decimal_places=4, null=True, blank=True)
    value = models.CharField('值', max_length=64, null=True, blank=True)
    value_type = models.SmallIntegerField('值类型', choices=ReportItem.VALUE_TYPES, null=True, blank=True)
    value_unit = models.SmallIntegerField('值单位', choices=ReportItem.UNIT_TYPES, null=True, blank=True)

    def __str__(self):
        return self.subject.name

    def get_value(self):
        if self.value_type == 1:
            return self.value_number, self.value_type

        return self.value, self.value_type

    class Meta:
        verbose_name = '报告期报表项目'
        verbose_name_plural = verbose_name

# INSERT into `basedata_reportitem_2008`(
# `value`, `value_number`, `value_type`,
# `value_unit`, `report_id`, `subject_id`
# ) SELECT
# `basedata_reportitem`.`value`, `basedata_reportitem`.`value_number`, `basedata_reportitem`.`value_type`,
# `basedata_reportitem`.`value_unit`, `basedata_reportitem`.`report_id`, `basedata_reportitem`.`subject_id`
# FROM `basedata_reportitem`
# left join `basedata_report` on `basedata_reportitem`.`report_id` = `basedata_report`.`id`
# where `basedata_report`.`year` = 2008;

# INSERT into `basedata_xreportitem_2008`(
# `value`, `value_number`, `value_type`,
# `value_unit`, `report_id`, `subject_id`
# ) SELECT
# `basedata_xreportitem`.`value`, `basedata_xreportitem`.`value_number`, `basedata_xreportitem`.`value_type`,
# `basedata_xreportitem`.`value_unit`, `basedata_xreportitem`.`report_id`, `basedata_xreportitem`.`subject_id`
# FROM `basedata_xreportitem`
# left join `basedata_xreport` on `basedata_xreportitem`.`report_id` = `basedata_xreport`.`id`
# where `basedata_xreport`.`year` = 2008;
