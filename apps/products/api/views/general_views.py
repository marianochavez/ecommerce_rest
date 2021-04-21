from apps.products.api.serializers.general_serializers import (
    CategoryProductSerializer, IndicatorSerializer, MeasureUnitSerializer)
from apps.base.api import GeneralListAPIView

from rest_framework import generics


class MeasureUnitListAPIView(GeneralListAPIView):
    """Show list of instances of MeasureUnit model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = MeasureUnitSerializer

class IndicatorListAPIView(GeneralListAPIView):
    """Show list of instances of Indicator model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = IndicatorSerializer

class CategoryProductListAPIView(GeneralListAPIView):
    """Show list of instances of CategoryProduct model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = CategoryProductSerializer