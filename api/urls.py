from django.urls import path, include
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
    path('api-auth/', include('rest_framework.urls')),
    # path('api/commodities/',CommodityListAPIView.as_view(), name='Commodities'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),    # API Schema:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),    # Optional UI:
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),     # Optional UI:
    path('hello/', HelloView.as_view(), name='hello'),    
    path("api/action/", BasicAPI.as_view()),
]