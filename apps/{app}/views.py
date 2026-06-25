"""
COVERDE - apps/{app}/views.py
Placeholder - a desenvolver em etapa posterior (Portugal).
"""

from django.shortcuts import render


def placeholder(request):
    return render(request, 'base.html', {
        'title': '{app_name}',
        'content': 'Página em desenvolvimento. Brevemente disponível.'
    })