from django.db import models


class Cart(models.Model):
    """Shopping cart (session-based)"""
    
    session_key = models.CharField(max_length=40, unique=True)
    items = models.JSONField(default=list, blank=True)  # [{product_id, quantity, price}, ...]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f'Cart {self.session_key}'


class CartItem(models.Model):
    """Individual cart items (denormalized for performance)"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('users.Product', on_delete=models.CASCADE)  # Product está em users app
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price snapshot at time of add
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cart_cartitem'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = [['cart', 'product']]
