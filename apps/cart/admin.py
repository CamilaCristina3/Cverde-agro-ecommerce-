from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('session_key',)
    readonly_fields = ('session_key', 'created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__session_key', 'product__name')
