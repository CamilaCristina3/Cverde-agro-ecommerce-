from django.db.models import Count, Q
from django.views.generic import TemplateView

from apps.products.models import Product
from apps.producers.models import Producer


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = (
            Product.objects.filter(available=True, producer__isnull=False)
            .select_related("producer")
            .order_by("-created_at")[:4]
        )
        categories = (
            Product.objects.filter(available=True, producer__isnull=False)
            .values("category")
            .annotate(count=Count("id"))
        )
        category_icons = {
            "Frutas": "🍓",
            "Legumes": "🥕",
            "Verduras": "🥬",
            "Hortaliças": "🌶️",
            "Grãos": "🌾",
            "Orgânicos": "🍃",
        }
        context["categories"] = [
            {
                "name": category["category"],
                "icon": category_icons.get(category["category"], "🟢"),
                "count": category["count"],
            }
            for category in categories
            if category["category"]
        ]
        context["local_producers"] = Producer.objects.filter(active=True).annotate(
            products=Count("products", filter=models.Q(products__available=True))
        )[:3]
        return context
