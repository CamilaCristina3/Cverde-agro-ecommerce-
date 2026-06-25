from django.db.models import Count, Q
from django.conf import settings
from django.views.generic import TemplateView

# ✅ Importações refactorizadas
from apps.categories.models import Category
from apps.users.models import Product  # Product está em users
from apps.producers.models import Producer


class HomeView(TemplateView):
    template_name = "home_simple.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Placeholder context - full implementation coming
        return context