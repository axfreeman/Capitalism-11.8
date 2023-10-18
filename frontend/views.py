from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
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
from .models import *
import requests

def commodities(request):    #pull data from Capitalism 11.8
    response = requests.get('http://localhost:8000/api/commodities')    #convert reponse data into json
    user=get_user(request)
    commodity_list = response.json()
    context={
        'commodity_list':commodity_list,
        'user':user,
    }
    return render(request, "commodity_api_list.html", context)    
