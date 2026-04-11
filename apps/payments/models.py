from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment #{self.pk} - {self.status}"
