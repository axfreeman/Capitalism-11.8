from django.urls import path, include
from .views import diversion
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'commodities', CommodityAPIView, 'Commodity')
router.register(r'simulations', SimulationAPIView, 'Simulation')
router.register(r'stocks', StockAPIView, 'Stock')
router.register(r'industries', IndustryAPIView, 'Industry')
router.register(r'classes', SocialClassAPIView, 'Social Class')
router.register(r'owners', OwnerAPIView, 'Owner')
router.register(r'trace', TraceAPIView, 'Trace')

urlpatterns = [
    path('api/', include(router.urls)),
    path('diversion/', diversion, name='APICommodities'), #TODO temporary, delete this when done
    path('apicommodities',CommodityAPIView.as_view({'get':'list'})),
    path('api-auth/', include('rest_framework.urls')),
    # API Schema:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]