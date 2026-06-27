"""
COVERDE - apps/{app}/urls.py
URLs placeholder (Portugal).
"""

from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('', views.placeholder, name='index'),
]
