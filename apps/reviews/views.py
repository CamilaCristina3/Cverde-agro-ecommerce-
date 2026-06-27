"""Views para gestão de avaliações (reviews) de produtos e produtores"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Q

from apps.users.models import Product, Producer
from apps.reviews.models import Review
from apps.orders.models import Order, OrderItem
from forms import ReviewForm


@login_required
@require_http_methods(["GET", "POST"])
def create_product_review(request, product_id):
    """Criar avaliação de um produto"""
    product = get_object_or_404(Product.objects.select_related("producer"), pk=product_id)
    
    # Verificar se utilizador já tem este produto numa encomenda
    has_purchased = OrderItem.objects.filter(
        product=product,
        order__customer=request.user,
        order__status__in=['delivered', 'confirmed', 'paid']
    ).exists()
    
    # Verificar se já tem avaliação
    existing_review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    if existing_review:
        messages.info(request, "Já avaliou este produto.")
        return redirect('products:detail', slug=product.slug)
    
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'reviews/create.html', {
            'form': form,
            'product': product,
            'has_purchased': has_purchased,
        })
    
    # POST - Guardar avaliação
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.verified_purchase = has_purchased
        review.is_approved = True  # Auto-approve para agora
        review.save()
        
        # Atualizar rating do produto
        _update_product_rating(product)
        
        messages.success(request, "A sua avaliação foi guardada com sucesso!")
        return redirect('products:detail', slug=product.slug)
    
    return render(request, 'reviews/create.html', {
        'form': form,
        'product': product,
        'has_purchased': has_purchased,
    })


@login_required
@require_http_methods(["GET", "POST"])
def create_producer_review(request, producer_id):
    """Criar avaliação de um produtor"""
    producer = get_object_or_404(Producer, pk=producer_id)
    
    # Verificar se utilizador já tem encomenda deste produtor
    has_purchased = Order.objects.filter(
        customer=request.user,
        items__product__producer=producer,
        status__in=['delivered', 'confirmed', 'paid']
    ).exists()
    
    # Verificar se já tem avaliação
    existing_review = Review.objects.filter(
        user=request.user,
        producer=producer
    ).first()
    
    if existing_review:
        messages.info(request, "Já avaliou este produtor.")
        return redirect('reviews:producer_list_uuid', producer_id=producer_id)
    
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'reviews/create.html', {
            'form': form,
            'producer': producer,
            'has_purchased': has_purchased,
        })
    
    # POST - Guardar avaliação
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.producer = producer
        review.verified_purchase = has_purchased
        review.is_approved = True  # Auto-approve para agora
        review.save()
        
        # Atualizar rating do produtor
        _update_producer_rating(producer)
        
        messages.success(request, "A sua avaliação foi guardada com sucesso!")
        return redirect('reviews:producer_list_uuid', producer_id=producer_id)
    
    return render(request, 'reviews/create.html', {
        'form': form,
        'producer': producer,
        'has_purchased': has_purchased,
    })


@login_required
def my_reviews(request):
    """Ver minhas avaliações"""
    reviews = Review.objects.filter(user=request.user).select_related('product', 'producer').order_by('-created_at')
    
    return render(request, 'reviews/my_reviews.html', {
        'reviews': reviews,
    })


def product_reviews(request, product_id):
    """Ver avaliações de um produto (pública)"""
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(
        product=product,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Estatísticas
    stats = reviews.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id'),
        five_star=Count('id', filter=Q(rating=5)),
        four_star=Count('id', filter=Q(rating=4)),
        three_star=Count('id', filter=Q(rating=3)),
        two_star=Count('id', filter=Q(rating=2)),
        one_star=Count('id', filter=Q(rating=1)),
    )
    
    return render(request, 'reviews/product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'stats': stats,
    })


def producer_reviews(request, producer_id):
    """Ver avaliações de um produtor (pública)"""
    producer = get_object_or_404(Producer, pk=producer_id)
    reviews = Review.objects.filter(
        producer=producer,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Estatísticas
    stats = reviews.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id'),
        five_star=Count('id', filter=Q(rating=5)),
        four_star=Count('id', filter=Q(rating=4)),
        three_star=Count('id', filter=Q(rating=3)),
        two_star=Count('id', filter=Q(rating=2)),
        one_star=Count('id', filter=Q(rating=1)),
    )
    
    return render(request, 'reviews/producer_reviews.html', {
        'producer': producer,
        'reviews': reviews,
        'stats': stats,
    })


def _update_product_rating(product):
    """Atualizar rating médio do produto"""
    reviews = Review.objects.filter(product=product, is_approved=True)
    avg = reviews.aggregate(Avg('rating'))['rating__avg']
    count = reviews.count()
    
    if avg:
        # Usar produto rating do produtor como referência (deprecated no modelo, mas pode estar em uso)
        pass  # Rating é calculado em tempo real, não armazenado


def _update_producer_rating(producer):
    """Atualizar rating médio do produtor"""
    reviews = Review.objects.filter(producer=producer, is_approved=True)
    avg = reviews.aggregate(Avg('rating'))['rating__avg']
    count = reviews.count()
    
    if avg:
        producer.rating = avg
        producer.total_ratings = count
        producer.save(update_fields=['rating', 'total_ratings'])
