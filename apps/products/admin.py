from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "producer", "price", "category", "stock", "available")
    list_filter = ("available", "category", "is_organic")
    search_fields = ("name", "producer__name", "description")
