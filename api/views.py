import requests
from django.shortcuts import render

from economy import actions

from .serializers import (
    CommoditySerializer, 
    SimulationSerializer, 
    StockSerializer, 
    IndustrySerializer, 
    SocialClassSerializer, 
    OwnerSerializer,
    TraceSerializer,
)
from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from economy.models import *
from rest_framework.permissions import IsAuthenticated 

class SimulationAPIView(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        headers = {'Authorization': 'Token dad43694d6bcb042d6f6fed0ac7f0f3d32be164b'}
        content = {'message': 'Hello, World!'}
        return Response(content,headers=headers)

class CommodityListAPIView(generics.ListAPIView):
    serializer_class = CommoditySerializer

    def get_queryset(self):
        user=self.request.user
        simulation=Simulation.objects.get(user=user)
        return Commodity.objects.filter(simulation=simulation)
    

class CommodityAPIView(viewsets.ModelViewSet):
    serializer_class = CommoditySerializer
    queryset = Commodity.objects.all()

    def get_context_data(self, **kwargs):
        logged_in_user=self.request.user
        print('Entering Commodity API View and getting user')
        context = super().get_context_data(**kwargs)
        qs=Commodity.objects.all() if logged_in_user.is_staff else Commodity.objects.filter(simulation__user=logged_in_user)
        context['commodity_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context      

class OwnerAPIView(viewsets.ModelViewSet):
    serializer_class=OwnerSerializer
    queryset = Owner.objects.all()

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

# POST views
    
class BasicAPI(APIView):
   
    # HERE IS THE POST API
    def post(self, request):
        req_data = request.data # Currently we ignore this because only use posts to ask for actions. Later might use it
        data = "Thank you. Your wish is my command"
        actions.admin_reset(request)
        return Response(data, status=status.HTTP_200_OK)
    