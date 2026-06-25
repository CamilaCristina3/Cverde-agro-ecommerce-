"""
COVERDE - apps/products/views.py
Views de produtos (Portugal).
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.users.models import Product, Category  # Product e Category estão em users


def product_list(request):
    """
    Lista de produtos com filtros (Portugal).
    """
    # Produtos aprovados e ativos
    products = Product.objects.filter(
        is_active=True,
        status='approved'  # Verificar se o modelo tem este campo
    ).select_related('store', 'category')

    # Categorias principais (sem pai)
    categories = Category.objects.filter(is_active=True, parent__isnull=True)

    # ========== FILTROS ==========
    cat_slug = request.GET.get('categoria')
    if cat_slug:
        try:
            cat = Category.objects.get(slug=cat_slug)
            products = products.filter(category=cat)
        except Category.DoesNotExist:
            pass

    # Filtro por preço (Portugal: Euro)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Filtro por pesquisa (Portugal)
    q = request.GET.get('q')
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(store__name__icontains=q)
        )

    # ========== ORDENAÇÃO ==========
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'title': 'Produtos',
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'q': q,
            'sort': sort,
        }
    })


def product_detail(request, slug):
    """
    Detalhe de um produto (Portugal).
    """
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
        status='approved'  # Verificar
    )

    # Produtos relacionados (mesma categoria)
    related = Product.objects.filter(
        category=product.category,
        is_active=True,
        status='approved'
    ).exclude(id=product.id)[:4]

    return render(request, 'products/detail.html', {
        'product': product,
        'related': related,
        'title': product.name
    })