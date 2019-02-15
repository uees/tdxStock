from django.db import models


class Industry(models.Model):
    """行业"""
    name = models.CharField(max_length=200)
    memo = models.CharField(max_length=256)


class Concept(models.Model):
    """概念"""
    name = models.CharField(max_length=200)
    memo = models.CharField(max_length=256)


class Territory(models.Model):
    """地域"""
    name = models.CharField(max_length=200)


class Section(models.Model):
    """版块"""
    name = models.CharField(max_length=200)
    memo = models.CharField(max_length=256)
