from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.shortcuts import redirect,render
from rest_framework.viewsets import ViewSet
from .models import *
import requests

def commodities(request):    #pull data from Capitalism 11.8
    url='http://localhost:8000/api/commodities'
    headers = {'Authorization': 'Token dad43694d6bcb042d6f6fed0ac7f0f3d32be164b'}
    response = requests.get(url,headers=headers)
    commodity_list = response.json()
    context={
        'commodity_list':commodity_list,
    }
    return render(request, "commodity_api_list.html", context)    
