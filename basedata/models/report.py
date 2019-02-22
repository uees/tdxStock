from django.db import models


class ReportType(models.Model):
    name = models.CharField('报告类型', max_length=200)
    memo = models.TextField('备注', null=True, blank=True)


class AccountingSubject(models.Model):
    name = models.CharField('科目名称', max_length=200)
    parent = models.ForeignKey('self', verbose_name='上级科目', on_delete=models.CASCADE)
    memo = models.TextField('备注', null=True, blank=True)


class Report(models.Model):
    VALUE_TYPES = [
        ('NUMBER', '数字'),
        ('STRING', '字符串'),
    ]
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    subject = models.ForeignKey(AccountingSubject, on_delete=models.CASCADE)
    year = models.IntegerField('年度')
    quarter = models.IntegerField('季度')
    value = models.TextField('值', null=True, blank=True)
    value_type = models.CharField('值数据类型', choices=VALUE_TYPES, max_length=64)
    value_unit = models.CharField('数据单位', max_length=64)
