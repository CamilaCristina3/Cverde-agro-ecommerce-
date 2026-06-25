def cart_count(request):
    """Disponibiliza contador do carrinho em todos os templates."""
    count = 0
    if request.user.is_authenticated:
        try:
            from apps.cart.models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                count = cart.item_count
        except Exception:
            pass
    return {'cart_item_count': count}