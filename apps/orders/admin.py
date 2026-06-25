from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("quantity",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    
    list_display = (
        "id",
        "customer",
        "created_at",
        "items_count",
    )
    
    list_filter = (
        "created_at",
    )
    
    search_fields = (
        "id",
        "customer__email",
        "customer__username",
    )
    
    readonly_fields = (
        "created_at",
    )
    
    fieldsets = (
        ("Informação da Encomenda", {
            "fields": (
                ("id", "user"),
                "created_at",
            )
        }),
    )
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Itens"
    
    date_hierarchy = "created_at"
    list_per_page = 25
