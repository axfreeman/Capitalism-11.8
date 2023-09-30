# see https://learndjango.com/tutorials/django-login-and-logout-tutorial
from django.urls import path, include
urlpatterns = [
  path('accounts/', include('django.contrib.auth.urls')),
]