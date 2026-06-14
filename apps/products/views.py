from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from apps.users.models import Producer, Product, Category
from django.conf import settings
from forms import ProductForm


def product_list(request):
    q = (request.GET.get("q") or "").strip()
    category_id = (request.GET.get("category") or "").strip()
    certification = (request.GET.get("certification") or "").strip()
    producer_id = (request.GET.get("producer") or "").strip()
    sort = (request.GET.get("sort") or "newest").strip()
    in_stock = (request.GET.get("in_stock") or "0").strip()  # default: mostrar todos

    products_qs = (
        Product.objects.filter(is_active=True, producer__is_active=True)
        .select_related("producer", "category")
        .order_by("-created_at")
    )

    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
            | Q(producer__name__icontains=q)
            | Q(producer__location__icontains=q)
        )

    if category_id.isdigit():
        products_qs = products_qs.filter(category_id=int(category_id))

    if certification:
        products_qs = products_qs.filter(certification=certification)

    if producer_id.isdigit():
        products_qs = products_qs.filter(producer_id=int(producer_id))

    if in_stock == "1":
        products_qs = products_qs.filter(stock__gt=0)

    if sort == "price_asc":
        products_qs = products_qs.order_by("price", "-created_at")
    elif sort == "price_desc":
        products_qs = products_qs.order_by("-price", "-created_at")
    elif sort == "rating_desc":
        products_qs = products_qs.order_by("-average_rating", "-total_reviews", "-created_at")
    elif sort == "name_asc":
        products_qs = products_qs.order_by("name", "-created_at")
    else:  # newest
        products_qs = products_qs.order_by("-created_at")

    total_products = products_qs.count()
    paginator = Paginator(products_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.filter(is_active=True).order_by("order", "name")
    # annotate categories with image_url: prefer uploaded image, otherwise use static placeholder
    for c in categories:
        try:
            if c.image and hasattr(c.image, 'url'):
                c.image_url = c.image.url
            else:
                c.image_url = settings.STATIC_URL + f"images/placeholders/categories/{c.slug}.svg"
        except Exception:
            c.image_url = settings.STATIC_URL + f"images/placeholders/categories/{c.slug}.svg"
    producers = Producer.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "products/list.html",
        {
            "page_obj": page_obj,
            "total_products": total_products,
            "categories": categories,
            "producers": producers,
            "current_path": request.get_full_path(),
            "filters": {
                "q": q,
                "category": category_id,
                "certification": certification,
                "producer": producer_id,
                "sort": sort,
                "in_stock": in_stock,
            },
        },
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("producer", "category"),
        pk=product_id,
        is_active=True,
        producer__is_active=True,
    )

    back = (request.GET.get("back") or "").strip()
    if back and url_has_allowed_host_and_scheme(
        url=back,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        back_url = back
    else:
        back_url = reverse("products:list")

    related_products = (
        Product.objects.filter(is_active=True, producer__is_active=True, category=product.category)
        .exclude(id=product.id)
        .select_related("producer", "category")
        .order_by("-created_at")[:6]
    )

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "related_products": related_products,
            "back_url": back_url,
        },
    )


@login_required
def create_product(request):
    """Create a new product for the logged-in producer."""
    try:
        producer = request.user.producer
    except Producer.DoesNotExist:
        messages.error(request, 'Precisa de um perfil de produtor para criar produtos.')
        return redirect('users:profile')

    if getattr(settings, "REQUIRE_PRODUCER_VERIFICATION", False) and not producer.is_verified:
        messages.warning(request, 'A verificação do produtor é necessária para publicar produtos.')
        return redirect('users:producer_panel')

    if not producer.is_verified:
        messages.info(request, "Conta de produtor ainda não verificada (opcional nesta fase). Pode publicar produtos.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.producer = producer
            product.save()
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect('products:list')
        else:
            messages.error(request, 'Erro ao criar o produto. Verifique os dados.')
    else:
        form = ProductForm()

    return render(request, 'products/create.html', {'form': form, 'producer': producer})
