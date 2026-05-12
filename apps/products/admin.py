from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "producer",
        "category",
        "price",
        "unit",
        "stock",
        "available",
        "is_organic",
        "created_at",
    )
    list_display_links = ("name",)

    list_filter = (
        "available",
        "is_organic",
        "category",
        "producer",
        ("created_at", admin.DateFieldListFilter),
    )

    search_fields = ("name", "producer__name", "description", "category")

    list_editable = ("price", "stock", "available")

    ordering = ("-created_at", "-id")

    list_per_page = 20
    date_hierarchy = "created_at"

    readonly_fields = ("created_at",)

    actions = [
        "mark_available",
        "mark_unavailable",
        "mark_organic",
        "mark_not_organic",
    ]

    fieldsets = (
        (_("Informação"), {"fields": ("producer", "name", "description", "category")}),
        (_("Preço"), {"fields": ("price", "unit")}),
        (_("Stock"), {"fields": ("stock", "available")}),
        (_("Certificação"), {"fields": ("is_organic",)}),
        (_("Metadados"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def mark_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"{updated} produto(s) marcado(s) como disponível(is).")

    mark_available.short_description = "Marcar como disponível"

    def mark_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"{updated} produto(s) marcado(s) como indisponível(is).")

    mark_unavailable.short_description = "Marcar como indisponível"

    def mark_organic(self, request, queryset):
        updated = queryset.update(is_organic=True)
        self.message_user(request, f"{updated} produto(s) marcado(s) como orgânico(s).")

    mark_organic.short_description = "Marcar como orgânico"

    def mark_not_organic(self, request, queryset):
        updated = queryset.update(is_organic=False)
        self.message_user(request, f"{updated} produto(s) marcado(s) como não orgânico(s).")

    mark_not_organic.short_description = "Marcar como não orgânico"
