from apps.products.api.serializers.general_serializers import (
    CategoryProductSerializer, IndicatorSerializer, MeasureUnitSerializer)
from apps.base.api import GeneralListAPIView

from rest_framework import generics
from rest_framework import viewsets


class MeasureUniViewSet(viewsets.ModelViewSet):
    """Show list of instances of MeasureUnit model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()


class IndicatorViewSet(viewsets.ModelViewSet):
    """Show list of instances of Indicator model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()

class CategoryProductViewSet(viewsets.ModelViewSet):
    """Show list of instances of CategoryProduct model

    Args:
        GeneralListAPIView (generics.ListAPIView): General View for list view where 
        queryset-->objects-state=True
    """
    serializer_class = CategoryProductSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()