"""
COVERDE - URLs principais do projeto (Portugal).
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def homepage(request):
    """Homepage com listagem de produtos em destaque (Portugal)."""
    from apps.users.models import Product
    from apps.categories.models import Category

    # Produtos em destaque (verificar se o campo existe)
    featured = Product.objects.filter(
        is_active=True,
        is_featured=True
    )[:8]

    # Últimos produtos adicionados
    recent = Product.objects.filter(
        is_active=True
    ).order_by('-created_at')[:12]

    # Categorias principais
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    )[:8]

    # Categorias padrão (fallback para Portugal)
    default_categories = [
        'Frutas', 'Legumes', 'Verduras', 'Orgânicos',
        'Grãos', 'Hortaliças', 'Vinho', 'Azeite'
    ]

    return render(request, 'home.html', {
        'featured_products': featured,
        'recent_products': recent,
        'categories': categories,
        'default_categories': default_categories,
        'title': 'COVERDE - Marketplace Agrícola de Portugal'  # ← Portugal
    })


# ========== PERSONALIZAR ADMIN ==========
admin.site.site_header = 'COVERDE - Administração'
admin.site.site_title = 'COVERDE Admin'
admin.site.index_title = 'Painel de Administração'


# ========== URLS ==========
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Homepage
    path('', homepage, name='home'),

    # Utilizadores
    path('utilizadores/', include('apps.users.urls', namespace='users')),

    # Produtores
    path('produtores/', include('apps.producers.urls', namespace='producers')),

    # Lojas
    path('lojas/', include('apps.stores.urls', namespace='stores')),

    # Produtos
    path('produtos/', include('apps.products.urls', namespace='products')),

    # Carrinho
    path('carrinho/', include('apps.cart.urls', namespace='cart')),

    # Encomendas
    path('encomendas/', include('apps.orders.urls', namespace='orders')),

    # Pagamentos
    path('pagamentos/', include('apps.payments.urls', namespace='payments')),

    # Avaliações (Portugal)
    path('avaliacoes/', include('apps.reviews.urls', namespace='reviews')),

    # Suporte
    path('suporte/', include('apps.support.urls', namespace='support')),

    # Páginas (privacidade, termos, etc)
    path('paginas/', include('apps.pages.urls', namespace='pages')),

    # Relatórios (Portugal)
    path('relatorios/', include('apps.reports.urls', namespace='reports')),

    # Entregas (Portugal) - adicionado
    path('entregas/', include('apps.deliveries.urls', namespace='deliveries')),
]

# ========== FICHEIROS ESTÁTICOS E MEDIA ==========
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)