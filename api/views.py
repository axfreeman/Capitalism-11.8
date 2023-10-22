import requests
from django.shortcuts import redirect,render

def diversion(request):    #fix this all up later
    return render(request, "dummy.html")    

# Create your views here.
from .serializers import (
    CommoditySerializer, 
    SimulationSerializer, 
    StockSerializer, 
    IndustrySerializer, 
    SocialClassSerializer, 
    OwnerSerializer,
    TraceSerializer,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect,render
from rest_framework import viewsets
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import loader
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from economy.models import *

class OwnerAPIView(viewsets.ModelViewSet):
    serializer_class=OwnerSerializer
    queryset = Owner.objects.all()

class CommodityAPIView(viewsets.ModelViewSet):
    serializer_class = CommoditySerializer
    queryset = Commodity.objects.all()

class CommodityItemsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'commodity_api_list.html'    

    def get(self, request, format=None):
        items = Commodity.objects.all()
        serializer = CommoditySerializer(items, many=True)
        return Response(serializer.data)        


class SimulationAPIView(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()
    
class StockAPIView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

class IndustryAPIView(viewsets.ModelViewSet):
    serializer_class = IndustrySerializer
    queryset = Industry.objects.all()

class SocialClassAPIView(viewsets.ModelViewSet):
    serializer_class = SocialClassSerializer
    queryset = SocialClass.objects.all()

class TraceAPIView(viewsets.ModelViewSet):
    serializer_class=TraceSerializer
    queryset=Trace.objects.all()

