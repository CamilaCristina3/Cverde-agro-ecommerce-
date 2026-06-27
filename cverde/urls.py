"""
COVERDE - URLs principais do projeto.
"""

import os
from urllib.parse import quote

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def homepage(request):
    """
    Homepage profissional do marketplace COVERDE.

    Usa:
    - categorias visuais em /media/categories/
    - produtos reais da tabela users_product
    - produtos visuais de demonstracao em /media/products e /static/images
      quando ainda nao ha produtos na base de dados
    """

    from apps.users.models import Product

    categories = [
        {
            "name": "Frutas",
            "slug": "frutas",
            "image": "/media/categories/frutas.png",
            "icon": "apple-alt",
        },
        {
            "name": "Legumes",
            "slug": "legumes",
            "image": "/media/categories/legumes.png",
            "icon": "carrot",
        },
        {
            "name": "Verduras",
            "slug": "verduras",
            "image": "/media/categories/verduras.png",
            "icon": "leaf",
        },
        {
            "name": "Organicos",
            "slug": "organicos",
            "image": "/media/categories/organicos.png",
            "icon": "seedling",
        },
        {
            "name": "Graos",
            "slug": "graos",
            "image": "/media/categories/graos.png",
            "icon": "wheat-awn",
        },
        {
            "name": "Hortalicas",
            "slug": "hortalicas",
            "image": "/media/categories/hortalicas.png",
            "icon": "basket-shopping",
        },
        {
            "name": "Vinho",
            "slug": "vinho",
            "image": "/media/categories/vinho.png",
            "icon": "wine-bottle",
        },
        {
            "name": "Azeite",
            "slug": "azeite",
            "image": "/media/categories/azeite.png",
            "icon": "bottle-droplet",
        },
    ]

    base_products = Product.objects.filter(is_active=True).select_related(
        "category",
        "producer",
    )

    featured_products = base_products.filter(
        is_featured=True,
    ).order_by("-created_at")[:8]

    recent_products = base_products.order_by("-created_at")[:16]

    demo_products = []
    products_dir = settings.MEDIA_ROOT / "products"
    static_images_dir = settings.BASE_DIR / "static" / "images"
    showcase_limit = 12

    # Ordem comercial da vitrine: frutas frescas -> horticolas/verduras -> despensa
    curated_showcase_static = [
        "Morango Bio.webp",
        "Abacate.webp",
        "Laranja.webp",
        "Ananás.webp",
        "Pêra.webp",
        "Maçã.png",
        "Uva.webp",
        "Cenouras Bio.png",
        "Alface.png",
        "Pimentão.png",
        "Milho Verde.jpg",
        "Azeite.webp",
    ]

    excluded_files = {
        "logo.png",
        "logo.jpg",
        "logo.jpeg",
        "logo.svg",
        "product_placeholder.svg",
        "product_placeholder.png",
        "product_placeholder.jpg",
        "product_placeholder.jpeg",
    }

    def collect_demo_from_folder(folder_path, url_prefix, curated_filenames=None):
        if not folder_path.exists():
            return

        preferred = []
        secondary = []
        file_index = {}

        for filename in sorted(os.listdir(folder_path)):
            filename_lower = filename.lower()

            if filename_lower in excluded_files:
                continue

            if filename_lower.startswith("optimized_"):
                continue

            if filename_lower.startswith("hero"):
                continue

            if not filename_lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
                continue

            file_index[filename_lower] = filename

            if filename_lower.endswith(".webp") or filename_lower.endswith(".jpg") or filename_lower.endswith(".jpeg"):
                preferred.append(filename)
            else:
                secondary.append(filename)

        ordered_files = []
        if curated_filenames:
            for curated in curated_filenames:
                file_name = file_index.get(curated.lower())
                if file_name:
                    ordered_files.append(file_name)

        for filename in preferred + secondary:
            if filename not in ordered_files:
                ordered_files.append(filename)

        for filename in ordered_files:
            if len(demo_products) >= showcase_limit:
                break

            product_name = (
                os.path.splitext(filename)[0]
                .replace("_", " ")
                .replace("-", " ")
                .title()
            )

            if url_prefix.endswith("/"):
                file_url = f"{url_prefix}{quote(filename)}"
            else:
                file_url = f"{url_prefix}/{quote(filename)}"

            demo_products.append(
                {
                    "name": product_name,
                    "image": file_url,
                    "price": "2.49",
                    "unit": "kg",
                    "producer": "Produtor COVERDE",
                }
            )

    collect_demo_from_folder(static_images_dir, f"{settings.STATIC_URL}images", curated_filenames=curated_showcase_static)
    if len(demo_products) < showcase_limit:
        collect_demo_from_folder(products_dir, f"{settings.MEDIA_URL}products")

    context = {
        "title": "COVERDE - Marketplace Agricola",
        "categories": categories,
        "featured_products": featured_products,
        "recent_products": recent_products,
        "demo_products": demo_products[:showcase_limit],
        "hero_image": "/media/categories/hero-frutas.png",
    }

    return render(request, "home.html", context)


admin.site.site_header = "COVERDE - Administracao"
admin.site.site_title = "COVERDE Admin"
admin.site.index_title = "Painel de Administracao"


urlpatterns = [
    path("", homepage, name="home"),
    path("admin/", admin.site.urls),
    path("utilizadores/", include("apps.users.urls", namespace="users")),
    path("produtores/", include("apps.producers.urls", namespace="producers")),
    path("lojas/", include("apps.stores.urls", namespace="stores")),
    path("produtos/", include("apps.products.urls", namespace="products")),
    path("carrinho/", include("apps.cart.urls", namespace="cart")),
    path("encomendas/", include("apps.orders.urls", namespace="orders")),
    path("pagamentos/", include("apps.payments.urls", namespace="payments")),
    path("avaliacoes/", include("apps.reviews.urls", namespace="reviews")),
    path("suporte/", include("apps.support.urls", namespace="support")),
    path("paginas/", include("apps.pages.urls", namespace="pages")),
    path("relatorios/", include("apps.reports.urls", namespace="reports")),
    path("entregas/", include("apps.deliveries.urls", namespace="deliveries")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
