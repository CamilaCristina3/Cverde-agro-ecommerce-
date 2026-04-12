from __future__ import annotations


def nav_cart_count(request):
    """
    Mostra a quantidade total de itens no carrinho (por sessão) na navbar.
    Evita criar sessão nova automaticamente: se não existir session_key, retorna 0.
    """

    try:
        session = getattr(request, "session", None)
        session_key = getattr(session, "session_key", None)
    except Exception:
        return {"nav_cart_count": 0}

    if not session_key:
        return {"nav_cart_count": 0}

    try:
        from apps.users.models import Cart
    except Exception:
        return {"nav_cart_count": 0}

    try:
        cart = Cart.objects.filter(session_key=session_key).only("items").first()
    except Exception:
        return {"nav_cart_count": 0}

    total = 0
    items = getattr(cart, "items", None) or []
    for item in items:
        try:
            total += int(item.get("quantity") or 0)
        except Exception:
            continue

    return {"nav_cart_count": total}

