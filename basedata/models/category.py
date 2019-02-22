from django.db import models


class Industry(models.Model):
    """行业"""
    name = models.CharField(max_length=200)
    memo = models.TextField()
    stocks = models.ManyToManyField('Stock', through='IndustryStock')


class IndustryStock(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    date_joined = models.DateField()


class Concept(models.Model):
    """概念"""
    name = models.CharField(max_length=200)
    memo = models.TextField()
    stocks = models.ManyToManyField('Stock', through='ConceptStock')


class ConceptStock(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    date_joined = models.DateField()


class Territory(models.Model):
    """地域"""
    name = models.CharField(max_length=200)


class Section(models.Model):
    """版块"""
    name = models.CharField(max_length=200)
    memo = models.TextField()
    stocks = models.ManyToManyField('Stock', through='SectionStock')


class SectionStock(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date_joined = models.DateField()
