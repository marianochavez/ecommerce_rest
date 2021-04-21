from apps.products.models import MeasureUnit,CategoryProduct,Indicator

from rest_framework import serializers

class MeasureUnitSerializer(serializers.ModelSerializer):
    """A `ModelSerializer` is just a regular `Serializer`, except that:

    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.

    """
    class Meta:
        model = MeasureUnit
        exclude = ('state','created_date','modified_date','deleted_date')

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProduct
        exclude = ('state','created_date','modified_date','deleted_date')

class IndicatorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Indicator
        exclude = ('state','created_date','modified_date','deleted_date')