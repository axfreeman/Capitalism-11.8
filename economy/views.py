from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import redirect,render
from rest_framework import viewsets
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import loader
from .models import *
from .actions import create_simulation_from_project


from .serializers import (
    CommoditySerializer, 
    SimulationSerializer, 
    StockSerializer, 
    IndustrySerializer, 
    SocialClassSerializer, 
    OwnerSerializer,
    TraceSerializer,
)

# def home(request):
#     template = 'home.html'
#     return render(request,template)
def home(request):
    template = 'home.html'
    return redirect("/economy")

@login_required
def economy_view(request):
    logged_in_user=request.user
    industries=Industry.objects.filter(simulation__user=logged_in_user)
    social_classes=SocialClass.objects.filter(simulation__user=logged_in_user)
    stocks=Stock.objects.filter(simulation__user=logged_in_user)
    context={}
    context["industries"]=industries
    context["social_classes"]=social_classes
    context["stocks"]=stocks
    template = loader.get_template('economy.html')
    return HttpResponse(template.render(context, request))

def userDashboard(request):
    template = loader.get_template('user-dashboard.html')
    context={}
    simulation_list=Simulation.objects.filter(user=request.user)
    project_list=Simulation.objects.filter(state="TEMPLATE")
    context["simulation_list"]=simulation_list
    context["project_list"]=project_list
    return HttpResponse(template.render(context, request))

def createSimulation(request,pk):
    create_simulation_from_project(request.user,pk)
    return redirect('/user-dashboard/')

class OwnerAPIView(viewsets.ModelViewSet):
    serializer_class=OwnerSerializer
    queryset = Owner.objects.all()

class CommodityAPIView(viewsets.ModelViewSet):
    serializer_class = CommoditySerializer
    queryset = Commodity.objects.all()

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

class SimulationListView(ListView):
    model=Simulation
    template_name='simulations.html'
    def get_context_data(self, **kwargs):
        logged_in_user=self.request.user
        context = super().get_context_data(**kwargs)
        qs=Simulation.objects.all() if logged_in_user.is_staff else Simulation.objects.filter(user=logged_in_user)
        context['simulation_list']=qs
        return context  
    
class CommodityListView(ListView):
    model=Commodity
    template_name='commodities.html'
    def get_context_data(self, **kwargs):
        logged_in_user=self.request.user
        context = super().get_context_data(**kwargs)
        qs=Commodity.objects.all() if logged_in_user.is_staff else Commodity.objects.filter(simulation__user=logged_in_user)
        context['commodity_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    

class StockListView(ListView):
    model=Stock
    template_name='stocks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Stock.objects.filter(simulation__user=logged_in_user).order_by('owner')
        context['stock_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    
    
class IndustryListView(ListView):
    model=Industry
    template_name='industries.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Industry.objects.filter(simulation__user=logged_in_user)
        context['industry_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    

class SocialClassListView(ListView):
    model=SocialClass
    template_name='social_classes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=SocialClass.objects.filter(simulation__user=logged_in_user) 
        context['social_class_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    
#TODO this should only be available to admin
class OwnerListView(ListView):
    model=Owner
    template_name='owners.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Owner.objects.all()
        context['owner_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    

class BuyerListView(ListView):
    model=Buyer
    template_name='buyers.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Buyer.objects.filter(simulation__user=logged_in_user).order_by('purchaseStock__owner')
        context['buyer_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    

class SellerListView(ListView):
    model=Seller
    template_name='sellers.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Seller.objects.filter(simulation__user=logged_in_user)
        context['seller_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context  
    
class TraceListView(ListView):
    model=Trace
    template_name='trace.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user=self.request.user
        qs=Trace.objects.all() #TODO tighten up to current user
        context['trace_list']=qs
        context['simulation']=qs.first().simulation.id if qs.exists() else 0
        return context    
    
#TODO detail views should be restricted to the ones that the logged in user is allowed to see

class SimulationDetailView(DetailView):
    model = Simulation
    template_name='simulation_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    


class CommodityDetailView(DetailView):
    model = Commodity
    template_name='commodity_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class IndustryDetailView(DetailView):
    model = Industry
    template_name='industry_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class SocialClassDetailView(DetailView):
    model = SocialClass
    template_name='socialclass_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class OwnerDetailView(DetailView):
    model = Owner
    template_name='owner_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    

class StockDetailView(DetailView):
    model = Stock
    template_name='stock_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

