from abc import ABC

from rest_framework import serializers

from tdxStock.abstract_models import DynamicModel

from .models.report import AccountingSubject, Report, ReportType, XReport
from .models.stock import Stock
from .models.category import Concept, Territory, Industry


class StockListingField(serializers.RelatedField, ABC):
    def to_representation(self, value):
        return {'name': value.name, 'code': value.code}


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = '__all__'


class IndustrySerializer(serializers.ModelSerializer):
    # stocks = StockListingField(many=True, read_only=True)
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = IndustrySerializer(obj.industry_set, many=True)
        return serializer.data

    class Meta:
        model = Industry
        fields = '__all__'


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
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
    stock = StockSerializer(read_only=True)
    report_type = ReportTypeSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'


class XReportSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    report_type = ReportTypeSerializer(read_only=True)

    class Meta:
        model = XReport
        fields = '__all__'


class DynamicReportItemSerializer(object):
    def __new__(cls, base_cls, year):
        new_cls_name = f"{base_cls.__name__}_{year}Serializer"
        model_cls = type(new_cls_name, (serializers.ModelSerializer,),
                         {'__module__': serializers.ModelSerializer.__module__})
        model_cls.subject = AccountingSubjectSerializer()

        model_cls.Meta = type("Meta", (object,), {
            "model": DynamicModel(base_cls, year),
            "fields": '__all__'
        })

        return model_cls
