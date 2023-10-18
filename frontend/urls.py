from django.contrib import admin
from django.urls import path, include
from .views import commodities

urlpatterns = [
    path('frontend/', commodities,name='APICommodities'),
]