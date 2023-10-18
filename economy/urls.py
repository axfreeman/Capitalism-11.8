from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from economy import views
from economy import actions

router = routers.DefaultRouter()
router.register(r'commodities', views.CommodityAPIView, 'Commodity')
router.register(r'simulations', views.SimulationAPIView, 'Simulation')
router.register(r'stocks', views.StockAPIView, 'Stock')
router.register(r'industries', views.IndustryAPIView, 'Industry')
router.register(r'classes', views.SocialClassAPIView, 'Social Class')
router.register(r'owners', views.OwnerAPIView, 'Owner')
router.register(r'trace', views.TraceAPIView, 'Trace')

urlpatterns = [
    path('simulations/',views.SimulationListView.as_view(), name='simulations'),
    path('user-dashboard/',views.userDashboard, name='user_dashboard'),
    path('initialize/', views.home,name='initialize'),
    path('create-simulation/', views.home, name='create-simulation'),
    path('create-simulation/<int:pk>', views.createSimulation, name='create-simulation'),
    path('select-simulation/<int:pk>', views.home, name='select-simulation'),
    path('delete-simulation/<int:pk>', views.home, name='delete-simulation'),
    path('restart-simulation/<int:pk>', views.home, name='restart-simulation'),
    path('',views.home),
    path('home/', views.home),
    path('api/', include(router.urls)),
    path('demand/',actions.set_demand_and_supply),
    path('trade/', actions.trade),
    path('retrace/',actions.restart_trace),
    path('setup/',actions.setup),
    path('admin-reset/',actions.admin_reset, name='admin-reset'),
    path('vp', actions.set_commodities_from_stocks),
    path('produce',actions.produce),
    path('trace/',views.TraceListView.as_view()),
    path('commodities/', views.CommodityListView.as_view(),name='commodity-list'),
    path('stocks/',views.StockListView.as_view()),
    path('industries/',views.IndustryListView.as_view()),
    path('owners/',views.OwnerListView.as_view()),
    path('social_classes/',views.SocialClassListView.as_view()),
    path('buyers/',views.BuyerListView.as_view()),
    path('sellers/',views.SellerListView.as_view()),
    path("commodities/<pk>/", views.CommodityDetailView.as_view()),    
    path("social_classes/<pk>/", views.SocialClassDetailView.as_view()),    
    path("industries/<pk>/", views.IndustryDetailView.as_view()),    
    path("stocks/<pk>/", views.StockDetailView.as_view()),
    path("owners/<pk>/", views.OwnerDetailView.as_view()),
    path("economy/",views.economy_view),
    path('simulations/<pk>',views.SimulationDetailView.as_view(), name='simulation'),
    path('apicommodities',views.CommodityAPIView.as_view({'get':'list'})),
]

