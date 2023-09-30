from django.test import TestCase
from .models import Stock

def totalMoney(simulation):
  total=0
  for m in Stock.objects.filter(simulation__id=simulation,usage_type="Money"):
    total+=m.size
  return total

