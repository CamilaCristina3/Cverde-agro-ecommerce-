"""
COVERDE - apps/payments/urls.py
URLs de pagamentos (Portugal).
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('encomenda/<uuid:order_id>/pagar/', views.payment_checkout, name='checkout'),
    path('confirmacao/<uuid:payment_id>/', views.payment_success, name='success'),
]
