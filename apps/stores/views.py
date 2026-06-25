"""
COVERDE - apps/stores/views.py
Views de lojas (Portugal).
"""

from django.shortcuts import render, get_object_or_404
from .models import Store


def store_list(request):
    """Lista de lojas ativas (Portugal)."""
    stores = Store.objects.filter(status=Store.Status.ACTIVE, is_active=True)
    return render(request, 'stores/list.html', {
        'stores': stores,
        'title': 'Lojas'
    })


def store_detail(request, slug):
    """Detalhe de uma loja (Portugal)."""
    store = get_object_or_404(Store, slug=slug, is_active=True)
    products = store.products.filter(status='approved', is_active=True)
    return render(request, 'stores/detail.html', {
        'store': store,
        'products': products,
        'title': store.name
    })