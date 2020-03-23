from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basedata.models import (Concept, Industry, Report, ReportType, Section,
                             Stock, Territory, XReport)
from basedata.serializers import (ConceptSerializer, IndustrySerializer,
                                  ReportSerializer, ReportTypeSerializer,
                                  SectionSerializer, StockSerializer,
                                  TerritorySerializer, XReportSerializer)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.get_queryset().order_by('id')
    serializer_class = StockSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('code', 'name')


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
        year, quarter = request.query_params.get('quarter').split('-')

        report = XReport.objects.select_related('stock', 'report_type') \
            .filter(Q(stock=stock) &
                    Q(report_type=report_type) &
                    Q(year=int(year)) &
                    Q(quarter=int(quarter))).first()
        serializer = XReportSerializer(report)
        return Response(serializer.data)
