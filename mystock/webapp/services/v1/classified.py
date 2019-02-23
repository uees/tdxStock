# -*- coding: utf-8 -*-
'''
Created on 2016年7月25日

@author: Wan

==========  ===============================================  ==================
HTTP 方法             URL                                              动作
==========  ===============================================  ==================
GET         http://[hostname]/todo/api/tasks            检索任务列表
GET         http://[hostname]/todo/api/tasks/[task_id]  检索某个任务
POST        http://[hostname]/todo/api/tasks            创建新任务
PUT         http://[hostname]/todo/api/tasks/[task_id]  更新任务
DELETE      http://[hostname]/todo/api/tasks/[task_id]  删除任务
==========  ================================================ ==================

'''
from flask_restful import Resource

from webapp.extensions import cache
from webapp.models.stock import (AreaClassified, ConceptClassified,
                                 GemClassified, Hs300, IndustryClassified,
                                 SmeClassified, StClassified, StockBasic, Sz50,
                                 Terminated, Zz500)

from . import api


class IndustryList(Resource):

    def get(self):
        industries = cache.get("industries")
        if industries is None:
            industries = IndustryClassified.objects\
                .only("c_name").distinct(field="c_name")

        return industries


class ConceptList(Resource):

    def get(self):
        concepts = cache.get("concepts")
        if concepts is None:
            concepts = ConceptClassified.objects\
                .only("c_name").distinct(field="c_name")
        return concepts


class AreaList(Resource):

    def get(self):
        area = cache.get("area")
        if area is None:
            area = AreaClassified.objects\
                .only("area").distinct(field="area")
        return area


class StockList(Resource):

    def get(self):
        return StockBasic.objects.to_json()


class SmeList(Resource):

    def get(self):
        return SmeClassified.objects.to_json()


class GemList(Resource):

    def get(self):
        return GemClassified.objects.to_json()


class Hs300List(Resource):

    def get(self):
        return Hs300.objects.to_json()


class Sz50List(Resource):

    def get(self):
        return Sz50.objects.to_json()


class Zz500List(Resource):

    def get(self):
        return Zz500.objects.to_json()


class StList(Resource):

    def get(self):
        return StClassified.objects.to_json()


class TerminatedList(Resource):

    def get(self):
        return Terminated.objects.to_json()


api.add_resource(IndustryList, '/industries', endpoint='industries')
api.add_resource(ConceptList, '/concepts', endpoint='concepts')
api.add_resource(AreaList, '/area', endpoint='area')
api.add_resource(StockList, '/stocks', endpoint='stocks')
api.add_resource(SmeList, '/sme', endpoint='sme')
api.add_resource(GemList, '/gem', endpoint='gem')
api.add_resource(Hs300List, '/hs300', endpoint='hs300')
api.add_resource(Sz50List, '/sz50', endpoint='sz50')
api.add_resource(Zz500List, '/zz500', endpoint='zz500')
api.add_resource(StList, '/st', endpoint='st')
api.add_resource(TerminatedList, '/terminated', endpoint='terminated')
