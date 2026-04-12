from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.users.models import Cart, Order, OrderItem, Product
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
def add_to_cart(request, product_id: int):
    cart_obj = _get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if product.stock <= 0:
        messages.error(request, "Este produto está esgotado.")
        return redirect("products:list")

    quantity = _safe_int(request.POST.get("quantity"), default=1)
    if quantity < 1:
        quantity = 1

    current_qty = 0
    for item in cart_obj.items:
        if int(item.get("product_id")) == product.id:
            current_qty = int(item.get("quantity") or 0)
            break

    new_qty = min(product.stock, current_qty + quantity)
    if new_qty <= current_qty:
        messages.warning(request, "Quantidade máxima em stock já adicionada ao carrinho.")
        return redirect("orders:cart")

    cart_obj.add_item(product.id, quantity=new_qty - current_qty)
    messages.success(request, f'"{product.name}" adicionado ao carrinho.')
    return redirect("orders:cart")


@require_POST
def update_cart_item(request, product_id: int):
    cart_obj = _get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    quantity = _safe_int(request.POST.get("quantity"), default=1)
    if quantity < 1:
        return remove_from_cart(request, product_id)

    quantity = min(quantity, product.stock)
    items = cart_obj.items
    for item in items:
        if int(item.get("product_id")) == product.id:
            item["quantity"] = int(quantity)
            break
    cart_obj.items = items
    cart_obj.save(update_fields=["items", "updated_at"])
    messages.success(request, "Carrinho atualizado.")
    return redirect("orders:cart")


@require_POST
def remove_from_cart(request, product_id: int):
    cart_obj = _get_or_create_cart(request)
    cart_obj.remove_item(int(product_id))
    messages.info(request, "Item removido do carrinho.")
    return redirect("orders:cart")


@require_POST
def clear_cart(request):
    cart_obj = _get_or_create_cart(request)
    cart_obj.clear()
    messages.info(request, "Carrinho esvaziado.")
    return redirect("orders:cart")


@login_required
def checkout(request):
    cart_obj = _get_or_create_cart(request)
    items, subtotal = _cart_items_and_subtotal(cart_obj)
    if not items:
        messages.warning(request, "O carrinho está vazio.")
        return redirect("products:list")

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

                order = Order.objects.create(
                    user=request.user,
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
                    vat=vat,
                    total=total,
                    status="pending",
                    shipping_address=form.cleaned_data["shipping_address"],
                    shipping_contact=form.cleaned_data["shipping_contact"],
                )

                for it in items:
                    p = locked_products[it["product"].id]
                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        quantity=it["quantity"],
                        price=it["unit_price"],
                        product_name=p.name,
                        producer_name=getattr(getattr(p, "producer", None), "name", ""),
                    )
                    p.stock = p.stock - it["quantity"]
                    p.save(update_fields=["stock"])

                order.generate_invoice_number()

            _send_order_emails(order)
            cart_obj.clear()
            messages.success(request, "Encomenda criada com sucesso.")
            return redirect("orders:detail", order_id=order.id)
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
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})


def _get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart_obj, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart_obj


def _cart_items_and_subtotal(cart_obj: Cart):
    raw_items = cart_obj.items or []
    product_ids = [int(i.get("product_id")) for i in raw_items if i.get("product_id") is not None]
    products = {p.id: p for p in Product.objects.filter(id__in=product_ids, is_active=True).select_related("producer", "category")}

    items = []
    subtotal = Decimal("0.00")
    for raw in raw_items:
        product_id = raw.get("product_id")
        if product_id is None:
            continue
        product = products.get(int(product_id))
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
            recipient_list=[order.user.email],
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
