"""
COVERDE - apps/users/views.py
Views de utilizadores.
"""

from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from forms import ConsumerRegisterForm, LoginForm
from forms import ProductForm, ProducerVerificationRequestForm
from forms import ProducerRegisterForm as MarketplaceProducerRegisterForm
from apps.orders.models import Order, OrderItem
from apps.stores.models import Store
from .forms import (
    AddressForm,
    UserProfileForm,
)
from .models import AccountActivationToken, Address, CustomerProfile, Producer, Product, SupplierProfile

User = get_user_model()


def _default_auth_backend_path():
    backends = getattr(settings, "AUTHENTICATION_BACKENDS", [])
    if backends:
        return backends[0]
    return "django.contrib.auth.backends.ModelBackend"


def register(request):
    """Escolha do tipo de conta a criar."""
    next_url = (request.GET.get("next") or "").strip()
    return render(request, "users/register.html", {"title": "Criar Conta", "next_url": next_url})


def register_client(request):
    """Registo de novo cliente."""
    if request.user.is_authenticated:
        return redirect("/")

    next_url = (request.GET.get("next") or request.POST.get("next") or "").strip()

    if request.method == "POST":
        form = ConsumerRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=True)
                user.is_active = True
                user.is_verified = True
                user.email_verified_at = timezone.now()
                user.save(update_fields=["is_active", "is_verified", "email_verified_at", "accepted_terms_at", "accepted_privacy_policy_at", "marketing_opt_in", "marketing_opt_in_at", "user_type", "password", "username", "first_name", "last_name", "email", "phone"])

                CustomerProfile.objects.create(user=user)
            login(request, user, backend=_default_auth_backend_path())
            messages.success(request, "Conta criada com sucesso. A sua conta já está ativa e verificada.")
            return redirect(next_url or "/")
    else:
        form = ConsumerRegisterForm()

    return render(
        request,
        "users/register_consumer.html",
        {"form": form, "title": "Criar Conta de Cliente", "next_url": next_url},
    )


def register_producer(request):
    """Registo de novo produtor."""
    if request.user.is_authenticated:
        return redirect("/")

    next_url = (request.GET.get("next") or request.POST.get("next") or "").strip()

    if request.method == "POST":
        form = MarketplaceProducerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=True)
                user.is_active = True
                user.is_verified = True
                user.email_verified_at = timezone.now()
                user.save(update_fields=["is_active", "is_verified", "email_verified_at", "accepted_terms_at", "accepted_privacy_policy_at", "marketing_opt_in", "marketing_opt_in_at", "user_type", "password", "username", "first_name", "last_name", "email", "phone"])

                Producer.objects.create(
                    user=user,
                    name=(
                        form.cleaned_data.get("producer_name")
                        or f"{user.first_name} {user.last_name}".strip()
                        or user.email
                    ),
                    description=form.cleaned_data.get("producer_description", ""),
                    location=form.cleaned_data.get("producer_location", ""),
                    nif=form.cleaned_data.get("nif", ""),
                    verification_document=form.cleaned_data.get("verification_document"),
                    status=Producer.Status.PENDING,
                    is_active=True,
                )

                SupplierProfile.objects.create(
                    user=user,
                    company_name=(
                        form.cleaned_data.get("producer_name")
                        or f"{user.first_name} {user.last_name}".strip()
                        or user.email
                    ),
                    nif=form.cleaned_data.get("nif", ""),
                    description=form.cleaned_data.get("producer_description", ""),
                    contact_phone=user.phone or "",
                    contact_email=user.email,
                    status=SupplierProfile.Status.PENDING,
                )

                producer_obj = Producer.objects.get(user=user)
                Store.objects.get_or_create(
                    producer=producer_obj,
                    defaults={
                        "owner": user,
                        "name": (form.cleaned_data.get("producer_name") or f"Loja de {user.first_name}" or "Loja COVERDE")[:200],
                        "description": form.cleaned_data.get("producer_description", ""),
                        "status": Store.Status.PENDING,
                        "is_active": True,
                        "email": user.email,
                        "phone": user.phone or "",
                    },
                )

            messages.info(
                request,
                "Registo de produtor submetido com sucesso e sessão iniciada automaticamente. "
                "A sua conta já está ativa; a equipa COVERDE irá validar o perfil de produtor "
                "antes de começar a vender.",
            )
            login(request, user, backend=_default_auth_backend_path())
            return redirect(next_url or "/")
    else:
        form = MarketplaceProducerRegisterForm()

    return render(
        request,
        "users/register_producer.html",
        {"form": form, "title": "Registar como Produtor", "next_url": next_url},
    )


def activate_account(request, token):
    """Ativação de conta via token de email."""
    token_obj = AccountActivationToken.objects.filter(
        Q(token=token) | Q(token=str(token).replace('-', ''))
    ).select_related("user").first()

    if token_obj is None:
        messages.error(request, "O link de ativação é inválido ou já não existe.")
        return redirect("users:login")

    if not token_obj.is_valid:
        if token_obj.is_used:
            messages.warning(request, "Este link de ativação já foi utilizado.")
        else:
            messages.error(request, "Este link de ativação expirou. Contacte suporte@coverde.pt.")
        return redirect("users:login")

    user = token_obj.user
    producer = Producer.objects.filter(user=user).first()

    with transaction.atomic():
        token_obj.mark_as_used()
        user.is_verified = True
        user.email_verified_at = timezone.now()
        user.save(update_fields=["is_verified", "email_verified_at"])

    if producer is None:
        login(request, user, backend=_default_auth_backend_path())
        messages.success(
            request,
            "Conta confirmada com sucesso. Bem-vindo a COVERDE.",
        )
        return redirect("/")

    messages.success(
        request,
        f"Email confirmado com sucesso. A sua conta de produtor "
        "está pendente de aprovação pela equipa COVERDE.",
    )
    return redirect("users:login")


def user_login(request):
    """Login de utilizador."""
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form_data = request.POST.copy()
        identifier = (form_data.get("username") or "").strip()

        # Permite login usando email, mesmo que o username interno seja diferente.
        if identifier:
            matched_user = User.objects.filter(email__iexact=identifier).first()
            if matched_user:
                form_data["username"] = matched_user.username

        form = LoginForm(request, data=form_data)

        if form.is_valid():
            user = form.get_user()
            producer = Producer.objects.filter(user=user).first()

            # Em desenvolvimento, não exigir confirmação de email.
            require_email_verification = getattr(
                settings,
                "REQUIRE_EMAIL_VERIFICATION",
                False
            )

            if require_email_verification and not getattr(user, "is_verified", False):
                messages.warning(
                    request,
                    "Por favor confirme o seu email antes de entrar. "
                    "Verifique a sua caixa de entrada.",
                )
                return render(
                    request,
                    "users/login.html",
                    {"form": form, "title": "Entrar no COVERDE"},
                )

            # Em desenvolvimento, produtor pendente pode entrar.
            # A aprovação controla apenas a venda/publicação, não o acesso à conta.
            if producer and producer.status == Producer.Status.PENDING:
                messages.info(
                    request,
                    "A sua conta de produtor está pendente de aprovação pela equipa COVERDE. "
                    "Pode aceder à sua conta, mas algumas funcionalidades de venda podem ficar limitadas.",
                )

            if producer and producer.status == Producer.Status.SUSPENDED:
                messages.error(
                    request,
                    "A sua conta foi suspensa. Contacte suporte@coverde.pt."
                )
                return render(
                    request,
                    "users/login.html",
                    {"form": form, "title": "Entrar no COVERDE"},
                )

            if producer and producer.status == Producer.Status.REJECTED:
                messages.error(
                    request,
                    "A sua conta de produtor foi rejeitada. Contacte suporte@coverde.pt."
                )
                return render(
                    request,
                    "users/login.html",
                    {"form": form, "title": "Entrar no COVERDE"},
                )

            login(request, user, backend=_default_auth_backend_path())

            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            next_url = request.POST.get("next") or request.GET.get("next") or "/"
            return redirect(next_url)
    else:
        form = LoginForm(request)

    return render(
        request,
        "users/login.html",
        {"form": form, "title": "Entrar no COVERDE"},
    )


def user_logout(request):
    """Terminar sessão."""
    logout(request)
    messages.success(request, "Sessão terminada com sucesso. Até breve.")
    return redirect("/")


@login_required
def profile(request):
    """Página de perfil do utilizador."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)

    addresses = request.user.addresses.all()
    producer = _get_current_producer(request)
    orders_count = request.user.orders.count() if hasattr(request.user, 'orders') else 0
    spent = request.user.orders.aggregate(total=Sum('total')).get('total') if hasattr(request.user, 'orders') else Decimal('0.00')
    spent = spent or Decimal('0.00')
    user_name = request.user.get_full_name().strip() or request.user.username or request.user.email

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "addresses": addresses,
            "title": "O Meu Perfil",
            "user_name": user_name,
            "orders_count": orders_count,
            "spent": f'€{spent:.2f}',
            "is_producer": producer is not None or getattr(request.user, 'user_type', '') == 'producer',
            "producer": producer,
        },
    )


@login_required
def profile_edit(request):
    """Editar perfil do utilizador."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/profile_edit.html", {"form": form, "title": "Editar Perfil"})


@login_required
def delete_account(request):
    """Desativar conta e anonimizar dados básicos do utilizador."""
    if request.method == "POST":
        timestamp = timezone.now()
        request.user.is_active = False
        request.user.first_name = "Conta"
        request.user.last_name = "Removida"
        request.user.email = f"deleted-{request.user.pk}@coverde.local"
        request.user.username = f"deleted-{request.user.pk}"
        request.user.phone = ""
        request.user.marketing_opt_in = False
        request.user.data_deleted_at = timestamp
        request.user.deletion_requested_at = timestamp
        request.user.save()
        logout(request)
        messages.success(request, "A sua conta foi desativada com sucesso.")
        return redirect("home")

    return render(request, "users/delete_account.html", {"title": "Eliminar Conta"})


@login_required
def add_address(request):
    """Adicionar morada de entrega."""
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Morada adicionada com sucesso.")
            return redirect("users:profile")
    else:
        form = AddressForm()

    return render(
        request,
        "users/address_form.html",
        {"form": form, "title": "Adicionar Morada"},
    )


@login_required
def product_list_redirect(request):
    return redirect("products:list")


@login_required
def producer_panel(request):
    producer = _get_current_producer(request)
    if producer is None:
        messages.warning(request, "A sua conta ainda não tem um perfil de produtor associado.")
        return redirect("users:profile")

    products_qs = Product.objects.filter(producer=producer).select_related("category").order_by("-created_at")
    recent_orders_qs = Order.objects.filter(items__product__producer=producer).select_related("customer").distinct().order_by("-created_at")[:5]
    recent_orders = [
        {
            "id": order.reference or str(order.id),
            "customer": order.customer.get_full_name().strip() or order.customer.email,
            "status": order.get_status_display(),
            "amount": f"€{order.total:.2f}",
        }
        for order in recent_orders_qs
    ]
    top_products = [
        {
            "rank": index,
            "name": product.name,
            "price": f"€{product.price:.2f}/{product.unit}",
            "sales": product.total_sold,
        }
        for index, product in enumerate(products_qs.order_by("-total_sold", "-rating", "name")[:5], start=1)
    ]

    active_products = products_qs.filter(is_active=True).count()
    low_stock_count = products_qs.filter(stock__lte=5).count()
    total_sales = OrderItem.objects.filter(product__producer=producer).aggregate(total=Sum("subtotal")).get("total") or Decimal("0.00")

    stats = [
        {"label": "Produtos ativos", "value": active_products, "detail": f"{products_qs.count()} no total", "icon": "📦"},
        {"label": "Stock baixo", "value": low_stock_count, "detail": "Produtos com 5 unidades ou menos", "icon": "⚠️"},
        {"label": "Vendas totais", "value": f"€{total_sales:.2f}", "detail": "Valor agregado das encomendas", "icon": "💶"},
        {"label": "Avaliação", "value": f"{producer.rating:.1f}/5", "detail": f"{producer.total_ratings} avaliações", "icon": "⭐"},
    ]

    readiness_steps = [
        {
            "label": "Perfil do produtor preenchido",
            "done": bool((producer.name or "").strip() and (producer.location or "").strip()),
        },
        {
            "label": "Pelo menos 1 produto ativo",
            "done": active_products > 0,
        },
        {
            "label": "Conta aprovada para vender",
            "done": producer.status == Producer.Status.APPROVED,
        },
    ]

    return render(
        request,
        "users/producer_panel.html",
        {
            "title": "Painel do Produtor",
            "producer": producer,
            "products": products_qs[:8],
            "stats": stats,
            "recent_orders": recent_orders,
            "top_products": top_products,
            "readiness_steps": readiness_steps,
            "require_producer_verification": producer.status != Producer.Status.APPROVED,
        },
    )


@login_required
def producer_verification(request):
    producer = _require_producer(request)
    if producer is None:
        return redirect("users:profile")

    if request.method == "POST":
        form = ProducerVerificationRequestForm(request.POST, request.FILES, instance=producer)
        if form.is_valid():
            producer = form.save(commit=False)
            if not producer.is_verified:
                producer.status = Producer.Status.PENDING
            producer.save()
            messages.success(request, "Pedido de verificação submetido com sucesso.")
            return redirect("users:producer_panel")
    else:
        form = ProducerVerificationRequestForm(instance=producer)

    return render(
        request,
        "users/producer_verification.html",
        {"form": form, "producer": producer, "title": "Verificação de Produtor"},
    )


@login_required
def producer_products(request):
    producer = _require_producer(request)
    if producer is None:
        return redirect("users:profile")

    products_qs = Product.objects.filter(producer=producer).select_related("category").order_by("-created_at")
    status_filter = (request.GET.get("status") or "").strip()
    low_stock_filter = (request.GET.get("low_stock") or "").strip()

    if status_filter == "active":
        products_qs = products_qs.filter(is_active=True)
    elif status_filter == "inactive":
        products_qs = products_qs.filter(is_active=False)

    if low_stock_filter == "1":
        products_qs = products_qs.filter(stock__lte=5)

    paginator = Paginator(products_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    all_products_qs = Product.objects.filter(producer=producer)
    return render(
        request,
        "products/producer_list.html",
        {
            "title": "Meus Produtos",
            "producer": producer,
            "page_obj": page_obj,
            "total_products": all_products_qs.count(),
            "active_products": all_products_qs.filter(is_active=True).count(),
            "low_stock_count": all_products_qs.filter(stock__lte=5).count(),
            "status_filter": status_filter,
            "low_stock_filter": low_stock_filter,
        },
    )


@login_required
def product_create(request):
    producer = _require_producer(request)
    if producer is None:
        return redirect("users:profile")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.producer = producer
            product.status = "active" if product.is_active else "inactive"
            product.save()
            messages.success(request, "Produto criado com sucesso.")
            return redirect("users:producer_products")
    else:
        form = ProductForm(initial={"is_active": True})

    return render(
        request,
        "products/create.html",
        {"form": form, "producer": producer, "is_edit": False, "title": "Novo Produto"},
    )


@login_required
def product_edit(request, product_id):
    producer = _require_producer(request)
    if producer is None:
        return redirect("users:profile")

    product = get_object_or_404(Product, pk=product_id, producer=producer)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.status = "active" if product.is_active else "inactive"
            product.save()
            messages.success(request, "Produto atualizado com sucesso.")
            return redirect("users:producer_products")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/edit.html",
        {"form": form, "product": product, "producer": producer, "is_edit": True, "title": "Editar Produto"},
    )


@login_required
def product_delete(request, product_id):
    producer = _require_producer(request)
    if producer is None:
        return redirect("users:profile")

    product = get_object_or_404(Product, pk=product_id, producer=producer)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produto eliminado com sucesso.")
        return redirect("users:producer_products")

    return render(
        request,
        "products/delete_confirm.html",
        {"product": product, "producer": producer, "title": "Eliminar Produto"},
    )


def _get_current_producer(request):
    if not request.user.is_authenticated:
        return None
    return Producer.objects.filter(user=request.user).first()


def _require_producer(request):
    producer = _get_current_producer(request)
    if producer is None:
        messages.warning(request, "É necessário ter um perfil de produtor para aceder a esta área.")
    return producer