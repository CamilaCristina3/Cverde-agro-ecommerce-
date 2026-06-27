from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlencode
from django.views.decorators.http import require_POST

# ✅ Importações corrigidas
from apps.cart.models import Cart  # Cart está em cart app
from apps.users.models import Product  # Product está em users
from apps.orders.models import Order, OrderItem
from apps.stores.models import Store
from forms import CheckoutForm


def cart(request):
    cart_obj = _get_or_create_cart(request)
    items, subtotal = _cart_items_and_subtotal(cart_obj)

    shipping_cost = _shipping_cost(subtotal)
    vat = _vat_cost(subtotal)
    total = subtotal + shipping_cost + vat

    return render(
        request,
        "orders/cart.html",
        {
            "cart": cart_obj,
            "items": items,
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "vat": vat,
            "total": total,
            "free_shipping_threshold": Decimal(str(getattr(settings, "FREE_SHIPPING_THRESHOLD_EUR", 50))),
        },
    )


@require_POST
def add_to_cart(request, product_id):
    cart_obj = _get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    next_url = (request.POST.get("next") or "").strip()

    if product.stock <= 0:
        messages.error(request, "Este produto está esgotado.")
        return _safe_redirect_next(request, next_url, fallback="products:list")

    quantity = _safe_int(request.POST.get("quantity"), default=1)
    if quantity < 1:
        quantity = 1

    current_qty = 0
    product_key = str(product.id)
    for item in cart_obj.items:
        if str(item.get("product_id")) == product_key:
            current_qty = int(item.get("quantity") or 0)
            break

    new_qty = min(product.stock, current_qty + quantity)
    if new_qty <= current_qty:
        messages.warning(request, "Quantidade máxima em stock já adicionada ao carrinho.")
        return _safe_redirect_next(request, next_url, fallback="orders:cart")

    _set_cart_item_quantity(cart_obj, product, new_qty)
    messages.success(request, f'"{product.name}" adicionado ao carrinho.')

    if not request.user.is_authenticated:
        messages.info(
            request,
            "Para finalizar a compra, registe-se como consumidor ou inicie sessão.",
        )
        register_url = reverse("users:register_consumer")
        return redirect(f"{register_url}?{urlencode({'next': reverse('orders:cart')})}")

    return _safe_redirect_next(request, next_url, fallback="orders:cart")


@require_POST
def update_cart_item(request, product_id):
    cart_obj = _get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    quantity = _safe_int(request.POST.get("quantity"), default=1)
    if quantity < 1:
        return remove_from_cart(request, product_id)

    quantity = min(quantity, product.stock)
    _set_cart_item_quantity(cart_obj, product, quantity)
    messages.success(request, "Carrinho atualizado.")
    return redirect("orders:cart")


@require_POST
def remove_from_cart(request, product_id):
    cart_obj = _get_or_create_cart(request)
    _remove_cart_item(cart_obj, product_id)
    messages.info(request, "Item removido do carrinho.")
    return redirect("orders:cart")


@require_POST
def clear_cart(request):
    cart_obj = _get_or_create_cart(request)
    cart_obj.items = []
    cart_obj.save(update_fields=["items", "updated_at"])
    messages.info(request, "Carrinho esvaziado.")
    return redirect("orders:cart")


def checkout(request):
    cart_obj = _get_or_create_cart(request)
    items, subtotal = _cart_items_and_subtotal(cart_obj)
    if not items:
        messages.warning(request, "O carrinho está vazio.")
        return redirect("products:list")

    if not request.user.is_authenticated:
        messages.info(request, "Para finalizar a compra, crie uma conta de consumidor ou inicie sessão.")
        register_url = reverse("users:register_consumer")
        next_target = request.get_full_path()
        if not url_has_allowed_host_and_scheme(
            url=next_target,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_target = reverse("orders:cart")
        return redirect(f"{register_url}?{urlencode({'next': next_target})}")

    shipping_cost = _shipping_cost(subtotal)
    vat = _vat_cost(subtotal)
    total = subtotal + shipping_cost + vat

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Revalidar stock e bloquear linhas
                product_ids = [it["product"].id for it in items]
                locked_products = {
                    p.id: p
                    for p in Product.objects.select_for_update().filter(id__in=product_ids)
                }
                for it in items:
                    p = locked_products.get(it["product"].id)
                    if p is None or not p.is_active:
                        messages.error(request, "Um dos produtos já não está disponível.")
                        return redirect("orders:cart")
                    if it["quantity"] > p.stock:
                        messages.error(request, f'Stock insuficiente para "{p.name}".')
                        return redirect("orders:cart")

                delivery_name = request.user.get_full_name().strip() or request.user.username or request.user.email
                shipping_address = form.cleaned_data["shipping_address"].strip()
                shipping_contact = form.cleaned_data["shipping_contact"].strip()

                order = Order.objects.create(
                    customer=request.user,
                    subtotal=subtotal,
                    delivery_fee=shipping_cost,
                    discount=Decimal("0.00"),
                    total=total,
                    status=Order.Status.PENDING,
                    delivery_name=delivery_name,
                    delivery_phone=shipping_contact,
                    delivery_street=shipping_address,
                    delivery_city="N/D",
                    delivery_district="N/D",
                    delivery_country="Portugal",
                )

                for it in items:
                    p = locked_products[it["product"].id]
                    store = _get_or_create_store_for_product(p)
                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        store=store,
                        quantity=it["quantity"],
                        unit_price=it["unit_price"],
                        product_unit=p.unit,
                        subtotal=it["line_total"],
                        product_name=p.name,
                    )
                    p.stock = p.stock - it["quantity"]
                    p.save(update_fields=["stock"])

            _send_order_emails(order)
            cart_obj.items = []
            cart_obj.save(update_fields=["items", "updated_at"])
            messages.success(request, "Encomenda criada com sucesso.")
            return redirect("payments:checkout", order_id=order.id)
        messages.error(request, "Não foi possível finalizar. Verifique os dados.")
    else:
        form = CheckoutForm(initial={"shipping_contact": getattr(request.user, "phone", "")})

    return render(
        request,
        "orders/checkout.html",
        {"items": items, "subtotal": subtotal, "shipping_cost": shipping_cost, "vat": vat, "total": total, "form": form},
    )


@login_required
def order_detail(request, order_id: int):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id, customer=request.user)
    vat_amount = (order.total - order.subtotal - order.delivery_fee + order.discount).quantize(Decimal("0.01"))
    if vat_amount < 0:
        vat_amount = Decimal("0.00")
    return render(request, "orders/detail.html", {"order": order, "vat_amount": vat_amount})


def _get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart_obj, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart_obj


def _cart_items_and_subtotal(cart_obj: Cart):
    raw_items = cart_obj.items or []
    product_ids = [str(i.get("product_id")) for i in raw_items if i.get("product_id") is not None]
    products = {
        str(p.id): p
        for p in Product.objects.filter(id__in=product_ids, is_active=True).select_related("producer", "category")
    }

    items = []
    subtotal = Decimal("0.00")
    for raw in raw_items:
        product_id = raw.get("product_id")
        if product_id is None:
            continue
        product = products.get(str(product_id))
        if product is None:
            continue
        quantity = _safe_int(raw.get("quantity"), default=1)
        if quantity < 1:
            continue
        quantity = min(quantity, int(product.stock or 0))
        unit_price = Decimal(str(product.price))
        line_total = unit_price * Decimal(quantity)
        subtotal += line_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )
    return items, subtotal.quantize(Decimal("0.01"))


def _shipping_cost(subtotal: Decimal):
    threshold = Decimal(str(getattr(settings, "FREE_SHIPPING_THRESHOLD_EUR", 50)))
    default_shipping = Decimal(str(getattr(settings, "DEFAULT_SHIPPING_COST_EUR", 5)))
    if subtotal >= threshold:
        return Decimal("0.00")
    return default_shipping.quantize(Decimal("0.01"))


def _vat_cost(subtotal: Decimal):
    rate = Decimal(str(getattr(settings, "VAT_RATE", 0)))
    if rate <= 0:
        return Decimal("0.00")
    return (subtotal * rate).quantize(Decimal("0.01"))


def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return int(default)


def _send_order_emails(order: Order):
    # Email ao consumidor
    try:
        order_url = reverse("orders:detail", kwargs={"order_id": order.id})
        absolute_url = order_url
        send_mail(
            subject=f"Encomenda #{order.id} criada - Coverde",
            message=(
                f"A sua encomenda foi criada com sucesso.\n\n"
                f"Total: €{order.total}\n"
                f"Estado: {order.get_status_display()}\n\n"
                f"Detalhes: {absolute_url}"
            ),
            from_email=None,
            recipient_list=[order.customer.email],
            fail_silently=True,
        )
    except Exception:
        pass

    # Email aos produtores (um email por produtor)
    producer_emails = set()
    for item in order.items.select_related("product__producer__user").all():
        producer_user = getattr(getattr(getattr(item.product, "producer", None), "user", None), "email", None)
        if producer_user:
            producer_emails.add(producer_user)

    for email in producer_emails:
        try:
            send_mail(
                subject=f"Nova encomenda #{order.id} - Coverde",
                message="Recebeu uma nova encomenda na plataforma Coverde. Consulte o painel de produtor para detalhes.",
                from_email=None,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass


def _safe_redirect_next(request, next_url: str, fallback: str):
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect(fallback)


def _set_cart_item_quantity(cart_obj: Cart, product: Product, quantity: int):
    product_key = str(product.id)
    items = list(cart_obj.items or [])

    for item in items:
        if str(item.get("product_id")) == product_key:
            item["quantity"] = int(quantity)
            break
    else:
        items.append({"product_id": product_key, "quantity": int(quantity)})

    cart_obj.items = items
    cart_obj.save(update_fields=["items", "updated_at"])


def _remove_cart_item(cart_obj: Cart, product_id):
    product_key = str(product_id)
    cart_obj.items = [
        item
        for item in (cart_obj.items or [])
        if str(item.get("product_id")) != product_key
    ]
    cart_obj.save(update_fields=["items", "updated_at"])


def _get_or_create_store_for_product(product: Product):
    producer = getattr(product, "producer", None)
    if producer is None:
        raise ValueError("Produto sem produtor associado")

    store = Store.objects.filter(producer=producer, is_active=True).order_by("created_at").first()
    if store:
        return store

    store_name = f"Loja de {producer.name}"[:200]
    return Store.objects.create(
        producer=producer,
        owner=producer.user,
        name=store_name,
        status=Store.Status.PENDING,
        is_active=True,
        email=producer.user.email,
    )
