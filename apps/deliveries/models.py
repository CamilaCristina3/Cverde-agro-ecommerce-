from django.db import models
from apps.orders.models import Order


class Delivery(models.Model):
    """Delivery tracking"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True)  # CTT, DHL, Fedex, etc
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'deliveries_delivery'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
    
    def __str__(self):
        order_ref = self.order.reference or str(self.order_id)
        return f'Delivery for order #{order_ref}'
