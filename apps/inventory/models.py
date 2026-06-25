from django.db import models
from apps.users.models import Product  # Product está em users


class InventoryLog(models.Model):
    """Track inventory movements"""
    
    MOVEMENT_TYPE_CHOICES = (
        ('add', 'Added'),
        ('remove', 'Removed'),
        ('adjustment', 'Adjustment'),
        ('purchase', 'Purchase'),
        ('return', 'Return'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_logs')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('users_auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inventory_inventorylog'
        verbose_name = 'Inventory Log'
        verbose_name_plural = 'Inventory Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.product.name} - {self.get_movement_type_display()}: {self.quantity}'


class StockAlert(models.Model):
    """Low stock alerts"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_alerts')
    threshold = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_stockalert'
        verbose_name = 'Stock Alert'
        verbose_name_plural = 'Stock Alerts'
