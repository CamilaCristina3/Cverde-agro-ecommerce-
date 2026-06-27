"""
COVERDE - apps/stores/urls.py
URLs de lojas (Portugal).
"""

from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.store_list, name='list'),
    path('<slug:slug>/', views.store_detail, name='detail'),
]
