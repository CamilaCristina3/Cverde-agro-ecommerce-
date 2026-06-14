from django.db.models import Count, Q
from django.conf import settings
from django.views.generic import TemplateView

from apps.users.models import Category, Producer, Product


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_products = Product.objects.filter(
            is_active=True,
            producer__is_active=True,
        ).select_related("producer", "category")

        featured_products = base_products.filter(is_featured=True, stock__gt=0).order_by("-created_at")[:8]
        if not featured_products:
            featured_products = base_products.filter(stock__gt=0).order_by("-created_at")[:8]
        context["featured_products"] = featured_products

        icon_map = {
            "frutas": "fas fa-apple-alt",
            "legumes": "fas fa-carrot",
            "verduras": "fas fa-leaf",
            "hortaliças": "fas fa-seedling",
            "horticulas": "fas fa-seedling",
            "grãos": "fas fa-wheat-awn",
            "organicos": "fas fa-certificate",
            "orgânicos": "fas fa-certificate",
        }

        categories_qs = (
            Category.objects.filter(is_active=True)
            .annotate(products_count=Count("products", filter=Q(products__is_active=True)))
            .filter(products_count__gt=0)
            .order_by("-products_count", "name")[:12]
        )
        context["categories"] = []
        for c in categories_qs:
            # prefer uploaded image, otherwise use static placeholder based on slug
            if getattr(c, "image", None):
                image_url = c.image.url if c.image else None
            else:
                image_url = settings.STATIC_URL + f"images/placeholders/categories/{c.slug}.svg"

            context["categories"].append(
                {
                    "id": c.id,
                    "name": c.name,
                    "count": c.products_count,
                    "icon_class": icon_map.get((c.name or "").strip().lower(), "fas fa-list"),
                    "image_url": image_url,
                }
            )

        context["local_producers"] = (
            Producer.objects.filter(is_active=True)
            .annotate(products_count=Count("products", filter=Q(products__is_active=True)))
            .filter(products_count__gt=0)
            .order_by("-rating", "name")[:5]
        )
        return context
