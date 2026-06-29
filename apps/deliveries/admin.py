from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'tracking_number', 'carrier', 'status', 'scheduled_date', 'delivered_date')
    list_filter = ('status', 'scheduled_date', 'delivered_date')
    search_fields = ('order__reference', 'tracking_number', 'carrier')
    readonly_fields = ('created_at', 'updated_at')
