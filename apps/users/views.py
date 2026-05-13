from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django.contrib.auth import login, logout
from django.conf import settings
import secrets
from urllib.parse import urlencode

from .models import Product, Producer, EmailVerificationToken, TwoFactorCode, Order, OrderItem
from forms import (
    LoginForm,
    TwoFactorVerifyForm,
    ProfileUpdateForm,
    ProducerVerificationRequestForm,
    ConsumerRegisterForm,
    ProducerRegisterForm,
)


def _send_email_verification(request, user):
    if not getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True):
        return
    token = EmailVerificationToken.objects.create(user=user)
    verify_url = request.build_absolute_uri(reverse("users:verify_email", kwargs={"token": str(token.token)}))
    send_mail(
        subject="Confirme o seu email - Coverde",
        message=f"Obrigado por se registar na Coverde.\n\nConfirme o seu email neste link:\n{verify_url}\n\nSe não foi você, ignore este email.",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


def _auto_verify_user_if_disabled(user):
    """
    Em ambientes onde os emails são fictícios/indisponíveis, permite criar contas
    sem confirmação por email quando REQUIRE_EMAIL_VERIFICATION=False.
    """
    if getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True):
        return
    if getattr(user, "is_verified", False):
        return
    user.is_verified = True
    user.email_verified_at = timezone.now()
    user.save(update_fields=["is_verified", "email_verified_at"])


def _dashboard_url_for_user(user):
    if user is None or not getattr(user, "is_authenticated", False):
        return reverse("users:login")
    if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False) or getattr(user, "user_type", None) == "admin":
        return reverse("admin:index")
    if getattr(user, "user_type", None) == "producer" or hasattr(user, "producer"):
        return reverse("users:producer_panel")
    return reverse("users:profile")


def _safe_next_url(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


@login_required
def dashboard(request):
    """Dashboard isolado por tipo de utilizador."""
    return redirect(_dashboard_url_for_user(request.user))


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = _safe_next_url(self.request)
        if next_url:
            return next_url
        return reverse("users:dashboard")
    
    def form_valid(self, form):
        """Handle remember me functionality"""
        remember_me = self.request.POST.get('remember_me')

        user = form.get_user()
        # Nota: o login não é condicionado por confirmação de email.
        # Em ambientes com email real, pode-se manter o fluxo de verificação como
        # um passo recomendado, mas não bloqueante.
        if getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True) and user and not getattr(user, "is_verified", False):
            _send_email_verification(self.request, user)
            messages.info(self.request, "Recomendamos confirmar o seu email. Enviámos um link de verificação.")

        if user and getattr(user, "two_factor_enabled", False):
            success_url = _safe_next_url(self.request) or reverse("users:dashboard")

            code = f"{secrets.randbelow(1000000):06d}"
            TwoFactorCode.issue(user, code, ttl_seconds=600)
            send_mail(
                subject="Código de verificação (2FA) - Coverde",
                message=f"O seu código de verificação é: {code}\n\nEste código expira em 10 minutos.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            self.request.session["two_factor_user_id"] = user.id
            self.request.session["two_factor_next"] = success_url
            self.request.session["two_factor_remember_me"] = bool(remember_me)
            messages.info(self.request, "Enviámos um código de verificação para o seu email.")
            return redirect("users:two_factor_verify")

        response = super().form_valid(form)
        
        if remember_me:
            # Keep session for 30 days (default is 2 weeks)
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            # Session expires when browser closes
            self.request.session.set_expiry(0)
        
        return response


class CustomLogoutView(LogoutView):
    next_page = 'home'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    
    def get_success_url(self):
        from django.urls import reverse
        return reverse('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    
    def get_success_url(self):
        from django.urls import reverse
        return reverse('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'



def register_choice(request):
    next_url = _safe_next_url(request)
    return render(
        request,
        "users/register.html",
        {
            "next_url": next_url,
            "require_email_verification": getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True),
        },
    )


def register_consumer(request):
    next_url = _safe_next_url(request)
    if request.method == 'POST':
        form = ConsumerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            _auto_verify_user_if_disabled(user)
            _send_email_verification(request, user)
            if getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True):
                messages.success(request, 'Conta criada com sucesso! Enviámos um link de confirmação para o seu email.')
            else:
                messages.success(request, 'Conta criada com sucesso! Já pode iniciar sessão.')
            login_url = reverse("users:login")
            if next_url:
                login_url = f"{login_url}?{urlencode({'next': next_url})}"
            return redirect(login_url)
    else:
        form = ConsumerRegisterForm()
    return render(request, 'users/register_consumer.html', {'form': form, 'next_url': next_url})


def register_producer(request):
    next_url = _safe_next_url(request)
    if request.method == 'POST':
        form = ProducerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Producer.objects.create(
                user=user,
                name=form.cleaned_data.get('producer_name', ''),
                description=form.cleaned_data.get('producer_description', ''),
                location=form.cleaned_data.get('producer_location', ''),
                nif=form.cleaned_data.get('nif', ''),
                verification_document=form.cleaned_data.get('verification_document'),
            )
            _auto_verify_user_if_disabled(user)
            _send_email_verification(request, user)
            if getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True):
                messages.success(request, 'Conta de produtor criada com sucesso! Enviámos um link de confirmação para o seu email.')
            else:
                messages.success(request, 'Conta de produtor criada com sucesso! Já pode iniciar sessão.')
            login_url = reverse("users:login")
            if next_url:
                login_url = f"{login_url}?{urlencode({'next': next_url})}"
            return redirect(login_url)
    else:
        form = ProducerRegisterForm()
    return render(request, 'users/register_producer.html', {'form': form, 'next_url': next_url})


def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.select_related("user").get(token=token, used_at__isnull=True)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, "Link inválido ou já utilizado.")
        return redirect("users:login")

    # Expiração simples (48 horas)
    if token_obj.created_at < timezone.now() - timedelta(hours=48):
        messages.error(request, "Este link expirou. Faça login para receber um novo link.")
        return redirect("users:login")

    user = token_obj.user
    user.is_verified = True
    user.email_verified_at = timezone.now()
    user.save(update_fields=["is_verified", "email_verified_at"])

    token_obj.used_at = timezone.now()
    token_obj.save(update_fields=["used_at"])

    messages.success(request, "Email confirmado com sucesso. Já pode iniciar sessão.")
    return redirect("users:login")


def two_factor_verify(request):
    user_id = request.session.get("two_factor_user_id")
    next_url = request.session.get("two_factor_next") or reverse("users:profile")
    remember_me = bool(request.session.get("two_factor_remember_me"))

    if not user_id:
        return redirect("users:login")

    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("users:login")

    if request.method == "POST":
        form = TwoFactorVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            code_obj = TwoFactorCode.objects.filter(user=user, used_at__isnull=True).order_by("-created_at").first()
            if not code_obj or not code_obj.verify(code):
                messages.error(request, "Código inválido ou expirado.")
            else:
                code_obj.used_at = timezone.now()
                code_obj.save(update_fields=["used_at"])

                login(request, user)
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

                for key in ("two_factor_user_id", "two_factor_next", "two_factor_remember_me"):
                    request.session.pop(key, None)
                messages.success(request, "Sessão iniciada com sucesso.")
                return redirect(next_url)
    else:
        form = TwoFactorVerifyForm()

    return render(request, "users/two_factor_verify.html", {"form": form, "email": user.email})


@login_required
def profile(request):
    if getattr(request.user, "is_staff", False) or getattr(request.user, "is_superuser", False) or getattr(request.user, "user_type", None) == "admin":
        return redirect("admin:index")
    if getattr(request.user, "user_type", None) == "producer" or hasattr(request.user, "producer"):
        return redirect("users:producer_panel")
    return render(request, "users/profile.html", {
        "user_name": request.user.get_full_name() or request.user.username,
        "is_producer": hasattr(request.user, "producer"),
        "orders_count": 8,
        "spent": "€320.40",
    })


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("users:profile")
        messages.error(request, "Não foi possível atualizar. Verifique os dados.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/profile_edit.html", {"form": form})


@login_required
def delete_account(request):
    if getattr(request.user, "is_staff", False) or getattr(request.user, "is_superuser", False) or getattr(request.user, "user_type", None) == "admin":
        messages.error(request, "Por segurança, contas de administração não podem ser eliminadas a partir do painel do utilizador.")
        return redirect("users:dashboard")
    if request.method == "POST":
        request.user.delete_account()
        logout(request)
        messages.success(request, "A sua conta foi eliminada (dados anonimizados) com sucesso.")
        return redirect("home")
    return render(request, "users/delete_account.html")


@login_required
def producer_panel(request):
    producer = getattr(request.user, "producer", None)
    if getattr(request.user, "is_staff", False) or getattr(request.user, "is_superuser", False) or getattr(request.user, "user_type", None) == "admin":
        return redirect("admin:index")
    if producer is None:
        messages.warning(request, "A sua conta não tem perfil de produtor.")
        return redirect("users:dashboard")

    from decimal import Decimal
    from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value
    from django.db.models.functions import Coalesce
    from django.utils import timezone

    products = Product.objects.filter(is_active=True, producer=producer).select_related("category").order_by("-created_at")
    in_stock_products = products.filter(stock__gt=0).count()

    # Encomendas associadas a este produtor (por itens)
    orders_qs = (
        Order.objects.filter(items__product__producer=producer)
        .select_related("user")
        .distinct()
    )

    # Definição pragmática de "vendas" nesta fase: somatório dos itens (preço * quantidade)
    # em encomendas não canceladas.
    sales_statuses = ("pending", "confirmed", "paid", "preparing", "shipped", "delivered")
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    line_total_expr = ExpressionWrapper(
        F("quantity") * F("price"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )

    def _sales_for(day):
        agg = (
            OrderItem.objects.filter(
                product__producer=producer,
                order__status__in=sales_statuses,
                order__created_at__date=day,
            )
            .aggregate(total=Sum(line_total_expr))
        )
        return (agg.get("total") or Decimal("0.00")).quantize(Decimal("0.01"))

    sales_today = _sales_for(today)
    sales_yesterday = _sales_for(yesterday)

    if sales_yesterday > 0:
        delta = ((sales_today - sales_yesterday) / sales_yesterday) * Decimal("100")
        sign = "+" if delta >= 0 else ""
        sales_detail = f"{sign}{delta.quantize(Decimal('1'))}% vs ontem"
    else:
        sales_detail = "— vs ontem"

    # Encomendas "ativas" (não canceladas)
    active_orders = orders_qs.filter(status__in=sales_statuses)
    active_orders_count = active_orders.count()
    new_orders_today = active_orders.filter(created_at__date=today, status="pending").count()

    recent_order_ids = (
        active_orders.order_by("-created_at").values_list("id", flat=True)[:10]
    )
    recent_items = (
        OrderItem.objects.filter(order_id__in=list(recent_order_ids), product__producer=producer)
        .select_related("order", "order__user")
    )

    per_order_totals = {}
    per_order_meta = {}
    for it in recent_items:
        per_order_totals[it.order_id] = per_order_totals.get(it.order_id, Decimal("0.00")) + (it.price * it.quantity)
        if it.order_id not in per_order_meta:
            user = it.order.user
            customer = user.get_full_name() or user.username or user.email
            per_order_meta[it.order_id] = {
                "id": f"#{it.order_id}",
                "customer": customer,
                "status": it.order.get_status_display(),
                "created_at": it.order.created_at,
            }

    recent_orders = []
    for order_id in recent_order_ids:
        meta = per_order_meta.get(order_id)
        if not meta:
            continue
        amount = (per_order_totals.get(order_id) or Decimal("0.00")).quantize(Decimal("0.01"))
        recent_orders.append(
            {
                "id": meta["id"],
                "customer": meta["customer"],
                "status": meta["status"],
                "amount": f"€{amount:.2f}",
            }
        )
        if len(recent_orders) >= 3:
            break

    top_products_qs = (
        Product.objects.filter(is_active=True, producer=producer)
        .annotate(
            sales_qty=Coalesce(
                Sum(
                    "order_items__quantity",
                    filter=Q(order_items__order__status__in=("paid", "shipped", "delivered")),
                ),
                Value(0),
            )
        )
        .order_by("-sales_qty", "-created_at")[:3]
    )
    top_products = []
    for idx, p in enumerate(top_products_qs, start=1):
        top_products.append(
            {
                "rank": idx,
                "name": p.name,
                "price": f"€{Decimal(str(p.price)):.2f}",
                "sales": int(p.sales_qty or 0),
            }
        )

    data = {
        "producer": producer,
        "products": products,
        "require_producer_verification": getattr(settings, "REQUIRE_PRODUCER_VERIFICATION", False),
        "stats": [
            {"label": "Vendas Hoje", "value": f"€{sales_today:.2f}", "detail": sales_detail, "icon": "📈", "class": "border-success"},
            {"label": "Encomendas", "value": str(active_orders_count), "detail": f"{new_orders_today} novas encomendas", "icon": "🛒", "class": "border-primary"},
            {"label": "Produtos", "value": str(products.count()), "detail": f"{in_stock_products} em stock", "icon": "📦", "class": "border-info"},
            {
                "label": "Avaliação",
                "value": f"{Decimal(str(getattr(producer, 'rating', 0) or 0)):.1f}",
                "detail": f"{int(getattr(producer, 'total_ratings', 0) or 0)} avaliações",
                "icon": "⭐",
                "class": "border-warning",
            },
        ],
        "recent_orders": recent_orders,
        "top_products": top_products,
    }
    return render(request, "users/producer_panel.html", data)


@login_required
def producer_verification_request(request):
    producer = getattr(request.user, "producer", None)
    if producer is None:
        messages.warning(request, "A sua conta não tem perfil de produtor.")
        return redirect("users:profile")

    if request.method == "POST":
        form = ProducerVerificationRequestForm(request.POST, request.FILES, instance=producer)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido de verificação submetido. Iremos analisar os documentos.")
            return redirect("users:producer_panel")
        messages.error(request, "Não foi possível submeter. Verifique os dados.")
    else:
        form = ProducerVerificationRequestForm(instance=producer)

    return render(request, "users/producer_verification.html", {"form": form, "producer": producer})
