# -*- coding: utf-8 -*-
'''
融资融券, 指数
'''
import tushare as ts
from flask_restful import Resource, reqparse

from webapp.models.stock import Distribution, Forecast, ShMargin, SzMargin

from . import api


class IndexList(Resource):

    def get(self):
        df = ts.get_index()
        if df is not None:
            return df.to_json(orient='records')


class KData(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ktype', type=str, location='json',
                                 default="D")
        self.parser.add_argument('autype', type=str, location='json',
                                 default="qfq")
        self.parser.add_argument('index', type=bool, location='json',
                                 default=False)
        self.parser.add_argument('start', type=str, location='json',
                                 default="")
        self.parser.add_argument('end', type=str, location='json',
                                 default="")
        super(KData, self).__init__()

    def get(self, code):
        args = self.parser.parse_args()
        df = ts.get_k_data(code=code, **args)
        if df is not None:
            return df.to_json(orient='records')


api.add_resource(KData, '/k/<string:code>')
