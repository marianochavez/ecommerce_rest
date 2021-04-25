from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_viewsets import ProductViewSet
from apps.products.api.views.general_views import *

router = DefaultRouter()

router.register(r'products',ProductViewSet,basename='products')
router.register(r'measure-units',MeasureUniViewSet,basename='measure-units')
router.register(r'indicators',IndicatorViewSet,basename='indicators')
router.register(r'category-products',CategoryProductViewSet,basename='category-products')

urlpatterns = router.urls