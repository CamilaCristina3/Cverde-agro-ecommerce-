from django.contrib import admin
from .models import SalesReport, CommissionReport


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'producer', 'period', 'start_date', 'end_date', 'total_revenue', 'total_orders')
    list_filter = ('period', 'start_date')
    search_fields = ('producer__company_name', 'producer__farm_name', 'producer__user__username')
    readonly_fields = ('generated_at',)


@admin.register(CommissionReport)
class CommissionReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'producer', 'period_start', 'period_end', 'commission_amount', 'status')
    list_filter = ('status', 'period_start')
    search_fields = ('producer__company_name', 'producer__farm_name', 'producer__user__username')
    readonly_fields = ('created_at',)
