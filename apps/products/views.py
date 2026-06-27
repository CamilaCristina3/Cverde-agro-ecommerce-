"""
COVERDE - apps/products/views.py
Views de produtos (Portugal).
"""

from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, Value, IntegerField
from apps.users.models import Product, Category  # Product e Category estão em users


FRUIT_SLUGS = {
    'frutas', 'fruta', 'fruits',
}

HORTI_SLUGS = {
    'hortalicas', 'hortícolas', 'horticolas', 'verduras', 'legumes', 'vegetais',
}

PANTRY_SLUGS = {
    'azeite', 'graos', 'grãos', 'mercearia', 'despensa',
}


def _market_group_data(category):
    slug = (getattr(category, 'slug', '') or '').lower()
    if slug in FRUIT_SLUGS:
        return {'key': 'fruits', 'label': 'Frutas frescas', 'icon': 'fa-apple-whole'}
    if slug in HORTI_SLUGS:
        return {'key': 'horti', 'label': 'Hortícolas e verduras', 'icon': 'fa-carrot'}
    if slug in PANTRY_SLUGS:
        return {'key': 'pantry', 'label': 'Despensa agrícola', 'icon': 'fa-bottle-droplet'}
    return {'key': 'others', 'label': 'Outros produtos', 'icon': 'fa-seedling'}


def product_list(request, category_slug=None):
    """
    Lista de produtos com filtros (Portugal).
    """
    current_path = request.get_full_path()

    products = Product.objects.filter(
        is_active=True,
        status='active',
    ).select_related('category')

    category_story_rank = Case(
        When(slug__in=FRUIT_SLUGS, then=Value(1)),
        When(slug__in=HORTI_SLUGS, then=Value(2)),
        When(slug__in=PANTRY_SLUGS, then=Value(3)),
        default=Value(9),
        output_field=IntegerField(),
    )

    categories = Category.objects.filter(is_active=True, parent__isnull=True).annotate(
        story_rank=category_story_rank
    ).order_by('story_rank', 'name')
    selected_category = None

    cat_slug = category_slug or request.GET.get('categoria')
    if cat_slug:
        try:
            selected_category = categories.get(slug=cat_slug)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None

    category_id = (request.GET.get('category') or '').strip()
    if category_id and selected_category is None:
        try:
            selected_category = categories.get(pk=category_id)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None

    min_price = _parse_decimal(request.GET.get('min_price'))
    max_price = _parse_decimal(request.GET.get('max_price'))
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    availability = (request.GET.get('availability') or '').strip()
    if availability == 'in_stock':
        products = products.filter(stock__gt=0)
    elif availability == 'featured':
        products = products.filter(is_featured=True)

    q = (request.GET.get('q') or '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q) |
            Q(producer__name__icontains=q) |
            Q(producer__location__icontains=q)
        )

    sort = (request.GET.get('sort') or request.GET.get('order') or 'market_story').strip()
    product_story_rank = Case(
        When(category__slug__in=FRUIT_SLUGS, then=Value(1)),
        When(category__slug__in=HORTI_SLUGS, then=Value(2)),
        When(category__slug__in=PANTRY_SLUGS, then=Value(3)),
        default=Value(9),
        output_field=IntegerField(),
    )

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating', '-total_reviews', '-created_at')
    elif sort == 'best_sellers':
        products = products.order_by('-total_sold', '-created_at')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.annotate(story_rank=product_story_rank).order_by(
            'story_rank',
            '-is_featured',
            '-total_sold',
            '-rating',
            'name',
        )

    total_products = products.count()
    in_stock_count = products.filter(stock__gt=0).count()
    featured_count = products.filter(is_featured=True).count()

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    show_group_headers = sort == 'market_story'
    page_cards = []
    previous_group_key = None

    for product in page_obj.object_list:
        group = _market_group_data(product.category)
        show_group = show_group_headers and group['key'] != previous_group_key
        page_cards.append({
            'product': product,
            'group': group,
            'show_group': show_group,
        })
        previous_group_key = group['key']

    query_params = request.GET.copy()
    query_params.pop('page', None)
    current_query = query_params.urlencode()

    return render(request, 'products/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'title': 'Produtos',
        'total_products': total_products,
        'in_stock_count': in_stock_count,
        'featured_count': featured_count,
        'selected_category': selected_category,
        'current_path': current_path,
        'current_query': current_query,
        'page_cards': page_cards,
        'show_group_headers': show_group_headers,
        'filters': {
            'category': category_id,
            'availability': availability,
            'min_price': '' if min_price is None else f'{min_price:.2f}',
            'max_price': '' if max_price is None else f'{max_price:.2f}',
            'q': q,
            'sort': sort,
        },
    })


def product_detail(request, slug):
    """
    Detalhe de um produto (Portugal).
    """
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
        status='active'
    )

    related = Product.objects.filter(
        category=product.category,
        is_active=True,
        status='active'
    ).select_related('producer', 'category').exclude(id=product.id)[:4]

    back_url = (request.GET.get('back') or request.META.get('HTTP_REFERER') or '').strip()
    if not back_url:
        back_url = '/produtos/'

    return render(request, 'products/detail.html', {
        'product': product,
        'related': related,
        'related_products': related,
        'back_url': back_url,
        'title': product.name
    })


def _parse_decimal(raw_value):
    value = (raw_value or '').strip()
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None
