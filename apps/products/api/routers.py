from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_viewsets import ProductViewSet
from apps.products.api.views.general_views import *

""" Provide functionality for automatically determining how the URLs for an application 
    should be mapped to the logic that deals with handling incoming requests.
"""
router = DefaultRouter()
"""router create automatic urls for crud
"""
router.register(r'products',ProductViewSet,basename='products')
router.register(r'measure-units',MeasureUniViewSet,basename='measure-units')
router.register(r'indicators',IndicatorViewSet,basename='indicators')
router.register(r'category-products',CategoryProductViewSet,basename='category-products')

#add routers to django urlpatterns
urlpatterns = router.urls