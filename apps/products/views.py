from django.db.models import Count, Prefetch, Q
from django.shortcuts import render

from apps.producers.models import Producer
from .models import Product


def product_list(request):
    producers = (
        Producer.objects.filter(active=True)
        .annotate(product_count=Count("products", filter=Q(products__available=True)))
        .filter(product_count__gt=0)
        .prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(available=True)
                .select_related("producer")
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
