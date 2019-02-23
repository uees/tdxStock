# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
from webapp.extensions import db


class Option(db.Document):
    name = db.StringField(unique=True)
    value = db.DynamicField()  # 动态数据类型
    note = db.StringField(max_length=200)
    meta = {'indexes': ['name'],
            'collection': 'option'}

    @staticmethod
    def get_option(name):
        op = Option.objects(name=name).first_or_404()
        return op.value
