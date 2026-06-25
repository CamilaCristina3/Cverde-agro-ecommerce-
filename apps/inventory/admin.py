from django.contrib import admin
from .models import InventoryLog, StockAlert


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'movement_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at',)


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'threshold', 'is_active', 'notified_at')
    list_filter = ('is_active', 'notified_at')
    search_fields = ('product__name',)
