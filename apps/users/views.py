"""
COVERDE - apps/users/views.py
Views de utilizadores (Portugal).
"""

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ClientRegisterForm, ProducerRegisterForm, CoverdeLoginForm, UserProfileForm, AddressForm
from .models import AccountActivationToken, CustomerProfile, Address
from .services import send_activation_email

User = get_user_model()


def register_client(request):
    """Registo de novo cliente (Portugal)."""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = User(
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone=form.cleaned_data.get('phone', ''),
                    role=User.Role.CLIENT,
                    status=User.Status.PENDING,
                    is_active=True,
                    is_email_verified=False,
                )
                user.set_password(form.cleaned_data['password'])
                user.save()

                # Criar perfil de cliente
                CustomerProfile.objects.create(user=user)

                # Criar token de ativação
                token = AccountActivationToken.objects.create(user=user)

                # Enviar email
                send_activation_email(request, user, token)

            messages.success(
                request,
                f'Conta criada com sucesso! Enviámos um email de confirmação para {user.email}. '
                f'Verifique a sua caixa de entrada (e spam) e clique no link para ativar a conta.'  # ← Portugal
            )
            return redirect('users:login')
    else:
        form = ClientRegisterForm()

    return render(request, 'users/register_client.html', {'form': form, 'title': 'Criar Conta de Cliente'})


def register_producer(request):
    """Registo de novo produtor (Portugal)."""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = ProducerRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = User(
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone=form.cleaned_data.get('phone', ''),
                    role=User.Role.PRODUCER,
                    status=User.Status.PENDING,
                    is_active=True,
                    is_email_verified=False,
                )
                user.set_password(form.cleaned_data['password'])
                user.save()

                # Criar perfil do produtor (Portugal)
                from apps.producers.models import ProducerProfile
                ProducerProfile.objects.create(
                    user=user,
                    company_name=form.cleaned_data.get('company_name', ''),
                    farm_name=form.cleaned_data.get('farm_name', ''),
                    district=form.cleaned_data.get('district', ''),  # ← Portugal: district
                    county=form.cleaned_data.get('county', ''),      # ← Portugal: county
                    status=ProducerProfile.Status.PENDING,
                )

                # Criar token de ativação
                token = AccountActivationToken.objects.create(user=user)

                # Enviar email
                send_activation_email(request, user, token)

            messages.info(
                request,
                f'Registo de produtor submetido! Enviámos um email de confirmação para {user.email}. '
                f'Depois de confirmar o email, a equipa COVERDE irá aprovar a sua conta.'
            )
            return redirect('users:login')
    else:
        form = ProducerRegisterForm()

    return render(request, 'users/register_producer.html', {'form': form, 'title': 'Registar como Produtor'})


def activate_account(request, token):
    """Ativação de conta via token de email (Portugal)."""
    token_obj = get_object_or_404(AccountActivationToken, token=token)

    if not token_obj.is_valid:
        if token_obj.is_used:
            messages.warning(request, 'Este link de ativação já foi utilizado.')  # ← Portugal
        else:
            messages.error(request, 'Este link de ativação expirou. Contacte suporte@coverde.pt')  # ← Portugal
        return redirect('users:login')

    user = token_obj.user

    with transaction.atomic():
        token_obj.mark_as_used()
        user.is_email_verified = True
        if user.role == User.Role.CLIENT:
            user.status = User.Status.ACTIVE
        user.save(update_fields=['is_email_verified', 'status'])

    if user.role == User.Role.CLIENT:
        login(request, user)
        messages.success(
            request,
            'Conta confirmada com sucesso. Bem-vindo(a) a COVERDE! '
            'Pode começar a comprar produtos agrícolas frescos.'
        )
        return redirect('/')
    else:
        messages.success(
            request,
            f'Email confirmado com sucesso! A sua conta de {user.get_role_display()} '
            f'está pendente de aprovação pela equipa COVERDE. '
            f'Será notificado(a) assim que a conta for aprovada.'
        )
        return redirect('users:login')


def user_login(request):
    """Login de utilizador (Portugal)."""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CoverdeLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.is_email_verified:
                messages.warning(
                    request,
                    'Por favor confirme o seu email antes de entrar. '
                    'Verifique a sua caixa de entrada.'
                )
                return render(request, 'users/login.html', {'form': form})

            if user.status == User.Status.PENDING and user.role != User.Role.CLIENT:
                messages.info(
                    request,
                    'A sua conta está pendente de aprovação pela equipa COVERDE. '
                    'Será contactado(a) brevemente.'
                )
                return render(request, 'users/login.html', {'form': form})

            if user.status == User.Status.SUSPENDED:
                messages.error(request, 'A sua conta foi suspensa. Contacte suporte@coverde.pt')  # ← Portugal
                return render(request, 'users/login.html', {'form': form})

            login(request, user)
            user.last_login_at = timezone.now()
            user.save(update_fields=['last_login_at'])

            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = CoverdeLoginForm(request)

    return render(request, 'users/login.html', {'form': form, 'title': 'Entrar no COVERDE'})


def user_logout(request):
    """Logout."""
    logout(request)
    messages.success(request, 'Sessão terminada com sucesso. Até breve!')
    return redirect('/')


@login_required
def profile(request):
    """Página de perfil do utilizador (Portugal)."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')  # ← Portugal
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    addresses = request.user.addresses.all()
    return render(request, 'users/profile.html', {
        'form': form,
        'addresses': addresses,
        'title': 'O Meu Perfil'
    })


@login_required
def add_address(request):
    """Adicionar morada de entrega (Portugal)."""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Morada adicionada com sucesso.')  # ← Portugal
            return redirect('users:profile')
    else:
        form = AddressForm()

    return render(request, 'users/address_form.html', {'form': form, 'title': 'Adicionar Morada'})  # ← Portugal