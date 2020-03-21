from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basedata.models import Industry, Stock
from basedata.serializers import IndustrySerializer, StockSerializer


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


class IndustryView(APIView):
    def get(self, request: Request, format=None):
        type = request.query_params.get('type', '证监会分类')
        industries = Industry.objects.prefetch_related('industry_set')\
            .filter(type=type).filter(parent__isnull=True).all()

        serializer = IndustrySerializer(industries, many=True)
        return Response(serializer.data)
