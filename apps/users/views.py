from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from apps.products.models import Product
from .forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'home'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, "users/profile.html", {
        "user_name": request.user.get_full_name() or request.user.username,
        "orders_count": 8,
        "spent": "€320.40",
    })


@login_required
def producer_panel(request):
    producer = getattr(request.user, "producer_profile", None)
    products = []
    if producer is not None:
        products = Product.objects.filter(available=True, producer=producer).order_by("-created_at")

    data = {
        "producer": producer,
        "products": products,
        "stats": [
            {"label": "Vendas Hoje", "value": "€192.50", "detail": "+12% vs ontem", "icon": "📈", "class": "border-success"},
            {"label": "Encomendas", "value": "12", "detail": "4 novas encomendas", "icon": "🛒", "class": "border-primary"},
            {"label": "Produtos", "value": str(products.count()), "detail": f"{products.count()} em stock", "icon": "📦", "class": "border-info"},
            {"label": "Avaliação", "value": "4.8", "detail": "127 avaliações", "icon": "⭐", "class": "border-warning"},
        ],
        "recent_orders": [
            {"id": "#2001", "customer": "Maria Santos", "amount": "€42.50", "status": "Novo", "status_class": "badge bg-success"},
            {"id": "#2002", "customer": "Pedro Costa", "amount": "€67.80", "status": "Em preparação", "status_class": "badge bg-warning text-dark"},
            {"id": "#2003", "customer": "Ana Silva", "amount": "€28.40", "status": "Enviado", "status_class": "badge bg-primary"},
        ],
        "top_products": [
            {"rank": 1, "name": "Tomate Cereja Orgânico", "price": "€8.50", "sales": 45},
            {"rank": 2, "name": "Alface Romana", "price": "€2.30", "sales": 40},
            {"rank": 3, "name": "Cenouras Bio", "price": "€3.20", "sales": 35},
        ],
    }
    return render(request, "users/producer_panel.html", data)
