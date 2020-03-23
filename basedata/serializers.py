from abc import ABC

from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from tdxStock.abstract_models import DynamicModel

from .models.category import Concept, Industry, Section, Territory
from .models.report import (AccountingSubject, Report, ReportItem, ReportType,
                            XReport, XReportItem)
from .models.stock import Stock


class StockListingField(serializers.RelatedField, ABC):
    def to_representation(self, value):
        return {'name': value.name, 'code': value.code, 'id': value.id}


# DynamicFieldsMixin 要在 ModelSerializer 前面
# ?omit=stocks,fields=name,id
class IndustrySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """行业 Serializer"""

    stocks = StockListingField(many=True, read_only=True)

    # children = serializers.SerializerMethodField('_get_children')
    # def _get_children(self, obj):
    #     serializer = IndustrySerializer(obj.industry_set, many=True)
    #     return serializer.data

    class Meta:
        model = Industry
        fields = "__all__"


class ConceptSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """概念 Serializer"""

    stocks = StockListingField(many=True, read_only=True)

    class Meta:
        model = Concept
        fields = '__all__'


class TerritorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """地域 Serializer"""

    stocks = StockListingField(many=True, read_only=True, source='stock_set')

    class Meta:
        model = Territory
        fields = '__all__'


class SectionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """版块 Serializer"""

    stocks = StockListingField(many=True, read_only=True)

    class Meta:
        model = Section
        fields = '__all__'


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = '__all__'


class AccountingSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingSubject
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    metas = serializers.JSONField()
    territory = TerritorySerializer()

    class Meta:
        model = Stock
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()  # 没指定 method_name, 则默认为 get_<field_name> 既 get_items
    stock = serializers.SerializerMethodField()
    report_type = ReportTypeSerializer()

    def get_items(self, report: Report):
        item_model = DynamicModel(ReportItem, report.year)
        item_serializer = DynamicReportItemSerializer(ReportItem, report.year)
        items = item_model.objects.select_related('subject').filter(report=report).all()
        serializer = item_serializer(items, many=True)
        return serializer.data

    def get_stock(self, report: Report):
        return {
            "id": report.stock.id,
            "name": report.stock.name,
            "code": report.stock.code,
        }

    class Meta:
        model = Report
        fields = '__all__'


class XReportSerializer(ReportSerializer):

    def get_items(self, report: XReport):
        item_model = DynamicModel(XReportItem, report.year)
        item_serializer = DynamicReportItemSerializer(XReportItem, report.year)
        items = item_model.objects.select_related('subject').filter(report=report).all()
        serializer = item_serializer(items, many=True)
        return serializer.data

    class Meta:
        model = XReport
        fields = '__all__'


class DynamicReportItemSerializer(object):
    def __new__(cls, base_cls, year):
        new_cls_name = f"{base_cls.__name__}_{year}Serializer"
        model_cls = type(new_cls_name, (serializers.ModelSerializer,), {
                             '__module__': serializers.ModelSerializer.__module__,
                             'subject': AccountingSubjectSerializer(),
                             'Meta': type("Meta", (object,), {
                                 "model": DynamicModel(base_cls, year),
                                 "fields": '__all__'
                                 })
                          })

        return model_cls
