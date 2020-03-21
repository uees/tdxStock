from rest_framework import serializers

from tdxStock.abstract_models import DynamicModel

from .models.stock import Stock
from .models.report import Report, XReport, ReportType, AccountingSubject


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = '__all__'


class AccountingSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingSubject
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
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
