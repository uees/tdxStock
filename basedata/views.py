from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basedata.models import Industry, Stock, Concept, Territory, Section
from basedata.serializers import IndustrySerializer, StockSerializer, ConceptSerializer, TerritorySerializer, \
    SectionSerializer


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


# todo report views
