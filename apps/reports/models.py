from django.db import models


class SalesReport(models.Model):
    """Daily/Monthly sales aggregations"""
    
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )
    
    producer = models.ForeignKey('users.Producer', on_delete=models.CASCADE, related_name='sales_reports', null=True, blank=True)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_items_sold = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports_salesreport'
        verbose_name = 'Sales Report'
        verbose_name_plural = 'Sales Reports'
        unique_together = [['producer', 'period', 'start_date', 'end_date']]


class CommissionReport(models.Model):
    """Platform commission calculations"""
    
    producer = models.ForeignKey('users.Producer', on_delete=models.CASCADE, related_name='commission_reports')
    period_start = models.DateField()
    period_end = models.DateField()
    gross_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    net_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('approved', 'Approved'), ('paid', 'Paid')])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports_commissionreport'
        verbose_name = 'Commission Report'
        verbose_name_plural = 'Commission Reports'
