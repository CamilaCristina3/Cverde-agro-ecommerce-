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
from datetime import timedelta
from django.contrib.auth import login, logout
from django.conf import settings
import secrets

from .models import Product, Producer, EmailVerificationToken, TwoFactorCode
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


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Handle redirect after successful login, including 'next' parameter"""
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        
        # Validate the next URL to prevent redirect attacks
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            return next_url

        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and hasattr(user, "producer"):
            return reverse("users:producer_panel")

        return reverse("users:profile")
    
    def form_valid(self, form):
        """Handle remember me functionality"""
        remember_me = self.request.POST.get('remember_me')

        user = form.get_user()
        if getattr(settings, "REQUIRE_EMAIL_VERIFICATION", True) and user and not getattr(user, "is_verified", False):
            _send_email_verification(self.request, user)
            messages.warning(self.request, "Confirme o seu email para iniciar sessão. Enviámos um novo link de verificação.")
            return redirect("users:login")

        if user and getattr(user, "two_factor_enabled", False):
            next_url = self.request.GET.get("next") or self.request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
            ):
                success_url = next_url
            elif hasattr(user, "producer"):
                success_url = reverse("users:producer_panel")
            else:
                success_url = reverse("users:profile")

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
    return render(request, 'users/register.html')


def register_consumer(request):
    if request.method == 'POST':
        form = ConsumerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            _send_email_verification(request, user)
            messages.success(request, 'Conta criada com sucesso! Enviámos um link de confirmação para o seu email.')
            return redirect('users:login')
    else:
        form = ConsumerRegisterForm()
    return render(request, 'users/register_consumer.html', {'form': form})


def register_producer(request):
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
            _send_email_verification(request, user)
            messages.success(request, 'Conta de produtor criada com sucesso! Enviámos um link de confirmação para o seu email.')
            return redirect('users:login')
    else:
        form = ProducerRegisterForm()
    return render(request, 'users/register_producer.html', {'form': form})


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
    if request.method == "POST":
        request.user.delete_account()
        logout(request)
        messages.success(request, "A sua conta foi eliminada (dados anonimizados) com sucesso.")
        return redirect("home")
    return render(request, "users/delete_account.html")


@login_required
def producer_panel(request):
    producer = getattr(request.user, "producer", None)
    if producer is None:
        messages.warning(request, "A sua conta não tem perfil de produtor.")
        return redirect("users:profile")
    products = []
    if producer is not None:
        products = Product.objects.filter(is_active=True, producer=producer).order_by("-created_at")

    data = {
        "producer": producer,
        "products": products,
        "stats": [
            {"label": "Vendas Hoje", "value": "€192.50", "detail": "+12% vs ontem", "icon": "📈", "class": "border-success"},
            {"label": "Encomendas", "value": "12", "detail": "4 novas encomendas", "icon": "🛒", "class": "border-primary"},
            {"label": "Produtos", "value": str(products.count()), "detail": f"{products.count()} em stock", "icon": "📦", "class": "border-info"},
            {"label": "Avaliação", "value": "4.8", "detail": "127 avaliações", "icon": "⭐", "class": "border-warning"},
        ],
        "recent_orders": [
            {"id": "#2001", "customer": "Maria Santos", "amount": "€42.50", "status": "Novo", "status_class": "badge bg-success"},
            {"id": "#2002", "customer": "Pedro Costa", "amount": "€67.80", "status": "Em preparação", "status_class": "badge bg-warning text-dark"},
            {"id": "#2003", "customer": "Ana Silva", "amount": "€28.40", "status": "Enviado", "status_class": "badge bg-primary"},
        ],
        "top_products": [
            {"rank": 1, "name": "Tomate Cereja Orgânico", "price": "€8.50", "sales": 45},
            {"rank": 2, "name": "Alface Romana", "price": "€2.30", "sales": 40},
            {"rank": 3, "name": "Cenouras Bio", "price": "€3.20", "sales": 35},
        ],
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
