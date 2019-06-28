from django.db import models


class Industry(models.Model):
    """行业"""
    parent = models.ForeignKey('self', verbose_name='父级行业', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('名称', max_length=200)
    type = models.CharField('类型', max_length=64, default="证监会分类")  # 申万分类
    memo = models.TextField('备注', null=True, blank=True)
    stocks = models.ManyToManyField('Stock', through='IndustryStock')

    def __str__(self):
        if self.parent:
            if self.parent.parent:
                return "%s -> %s -> %s" % (self.parent.parent.name, self.parent.name, self.name)

            return "%s -> %s" % (self.parent.name, self.name)

        return self.name

    class Meta:
        verbose_name = '行业'
        verbose_name_plural = verbose_name

        indexes = [
            models.Index(fields=['type'], name='type_idx'),
        ]


class IndustryStock(models.Model):
    stock = models.ForeignKey('Stock', verbose_name='股票', on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, verbose_name='行业', on_delete=models.CASCADE)
    date_joined = models.DateField('加入日期', null=True, blank=True)


class Concept(models.Model):
    """概念"""
    name = models.CharField("名称", max_length=200)
    memo = models.TextField('备注', null=True, blank=True)
    stocks = models.ManyToManyField('Stock', through='ConceptStock')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '概念'
        verbose_name_plural = verbose_name


class ConceptStock(models.Model):
    stock = models.ForeignKey('Stock', verbose_name="股票", on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, verbose_name="概念", on_delete=models.CASCADE)
    date_joined = models.DateField('加入日期', null=True, blank=True)


class Territory(models.Model):
    """地域"""
    name = models.CharField("名称", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '地域'
        verbose_name_plural = verbose_name


class Section(models.Model):
    """版块"""
    name = models.CharField("名称", max_length=200)
    memo = models.TextField('备注', null=True, blank=True)
    stocks = models.ManyToManyField('Stock', through='SectionStock')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '版块'
        verbose_name_plural = verbose_name


class SectionStock(models.Model):
    stock = models.ForeignKey('Stock', verbose_name="股票", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name="版块", on_delete=models.CASCADE)
    date_joined = models.DateField('加入日期', null=True, blank=True)
