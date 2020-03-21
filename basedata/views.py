from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from basedata.models import Stock, Industry
from basedata.serializers import StockSerializer, IndustrySerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.get_queryset().order_by('id')
    serializer_class = StockSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('code', 'name')


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.get_queryset()
    serializer_class = IndustrySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
