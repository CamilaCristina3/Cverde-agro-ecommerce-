from django.db.models import Count, Prefetch, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.users.models import Producer, Product
from forms import ProductForm


def product_list(request):
    producers = (
        Producer.objects.filter(is_active=True)
        .annotate(product_count=Count("products", filter=Q(products__is_active=True)))
        .filter(product_count__gt=0)
        .prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(is_active=True)
                .select_related("producer", "category")
                .order_by("-created_at"),
                to_attr="available_products",
            )
        )
        .order_by("name")
    )

    total_products = sum(producer.product_count for producer in producers)
    return render(
        request,
        "products/list.html",
        {"producers": producers, "total_products": total_products},
    )


@login_required
def create_product(request):
    """Create a new product for the logged-in producer."""
    try:
        producer = request.user.producer
    except Producer.DoesNotExist:
        messages.error(request, 'Precisa de um perfil de produtor para criar produtos.')
        return redirect('users:profile')

    if not producer.is_verified:
        messages.warning(request, 'A verificação do produtor é necessária para publicar produtos.')
        return redirect('users:producer_panel')

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
