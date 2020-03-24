from django.db.models import Q, F, CharField, Value, ExpressionWrapper
from django.db.models.functions import Concat
from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basedata.models import (Concept, Industry, Report, ReportType, Section,
                             Stock, Territory, XReport, ReportItem, XReportItem, AccountingSubject)
from basedata.serializers import (ConceptSerializer, IndustrySerializer,
                                  ReportSerializer, ReportTypeSerializer,
                                  SectionSerializer, StockSerializer,
                                  TerritorySerializer, XReportSerializer, AccountingSubjectSerializer,
                                  DynamicReportItemSerializer)
from tdxStock.abstract_models import DynamicModel


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.get_queryset().select_related('territory')
    serializer_class = StockSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('code', 'name')


class AccountingSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountingSubject.objects.select_related('report_type')
    serializer_class = AccountingSubjectSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.get_queryset()
    serializer_class = IndustrySerializer
    filter_fields = ('type',)
    pagination_class = None


class ConceptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Concept.objects.get_queryset()
    serializer_class = ConceptSerializer
    pagination_class = None


class TerritoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Territory.objects.get_queryset()
    serializer_class = TerritorySerializer
    pagination_class = None


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.get_queryset()
    serializer_class = SectionSerializer
    pagination_class = None


class ReportTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportType.objects.get_queryset()
    serializer_class = ReportTypeSerializer
    pagination_class = None


class ReportView(APIView):
    def get(self, request: Request, format=None):
        stock = request.query_params.get('stock')
        report_type = request.query_params.get('report_type')
        year, quarter = request.query_params.get('quarter').split('-')

        report = Report.objects.select_related('stock', 'report_type') \
            .filter(Q(stock=stock) &
                    Q(report_type=report_type) &
                    Q(year=int(year)) &
                    Q(quarter=int(quarter))).first()
        serializer = ReportSerializer(report)
        return Response(serializer.data)


class XReportView(APIView):
    def get(self, request: Request, format=None):
        stock = request.query_params.get('stock')
        report_type = request.query_params.get('report_type')
        quarter_str = request.query_params.get('quarter').split('-')

        if not stock or not report_type or not quarter_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        year, quarter = quarter_str.split('-')

        report = XReport.objects.select_related('stock', 'report_type') \
            .filter(Q(stock=stock) &
                    Q(report_type=report_type) &
                    Q(year=int(year)) &
                    Q(quarter=int(quarter))).first()
        serializer = XReportSerializer(report)
        return Response(serializer.data)


class CompareView(APIView):
    """给定一组股票, 比较他们的指标"""

    def get(self, request: Request, format=None):
        stocks = request.query_params.get('stocks')
        subject = request.query_params.get('subject')
        is_single = request.query_params.get('single', False)  # 是否单季度报
        quarter = request.query_params.get('quarter')  # 季度

        if not stocks or not subject:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        report_item_class = ReportItem if is_single else XReportItem
        report_class = Report if is_single else XReport

        stock_ids = stocks.split(',')
        # stocks = Stock.objects.filter(id__in=stock_ids).only('id', 'name', 'code').all()

        subject = AccountingSubject.objects.get(pk=subject)

        # 1. get all reports
        reports = report_class.objects.filter(stock__in=stock_ids).filter(report_type=subject.report_type).all()

        # todo 修复低效的多次查询
        report_items = []
        for report in reports:
            item_model = DynamicModel(report_item_class, report.year)
            qs = item_model.objects.select_related('report', 'subject') \
                .annotate(quarter=ExpressionWrapper(Concat(F('report__year'), Value('-'), F('report__quarter')),
                                                    output_field=CharField())) \
                .filter(subject_id=subject.id) \
                .filter(report_id=report.id)

            if quarter:
                qs = qs.filter(report__quarter=quarter)

            item = qs.first()

            serializer_class = DynamicReportItemSerializer(report_item_class, report.year)

            if item:
                report_items.append(serializer_class(item).data)

        return Response(report_items)

        # 2. use reports and subject to select report_items
        # items_queryset = self.get_items_queryset(reports, report_item_class)

        # items_queryset = items_queryset.select_related('report', 'report__stock') \
        #    .annotate(quarter=ExpressionWrapper(Concat(F('report__year'), Value('-'), F('report__quarter')),
        #                                        output_field=CharField())) \
        #    .filter(subject_id=subject.id)

        # if quarter:
        #    items_queryset = items_queryset.filter(report__quarter=quarter)

        # report_items = items_queryset.all()
        # return Response(report_items.values())

    def get_items_queryset(self, reports, report_item_class):
        qs = None
        for report in reports:
            item_model = DynamicModel(report_item_class, report.year)
            if qs is None:
                qs = item_model.objects.filter(report_id=report.id)
            else:
                qs = qs.union(item_model.objects.filter(report_id=report.id))

        return qs
