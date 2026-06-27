"""
COVERDE - apps/users/services.py
Serviços de utilizadores (Portugal).
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


def send_activation_email(request, user, token):
    """
    Enviar email de ativação de conta.
    
    Args:
        request: HttpRequest atual
        user: Instância do User
        token: Instância ou valor do token de ativação
    """
    subject = 'Confirme o seu email - Cverde'

    token_value = getattr(token, 'token', token)
    activation_path = reverse('users:activate', kwargs={'token': token_value})
    if request is not None:
        activation_url = request.build_absolute_uri(activation_path)
        domain = request.get_host()
    else:
        domain = getattr(settings, 'DOMAIN', 'http://127.0.0.1:8000').rstrip('/')
        activation_url = f'{domain}{activation_path}'
    
    account_type_label = dict(getattr(user, "USER_TYPE_CHOICES", [])).get(
        getattr(user, "user_type", "consumer"),
        "Conta",
    )
    is_pending_validation = getattr(user, "user_type", "consumer") in {"producer", "supplier"}
    support_email = getattr(settings, "SUPPORT_EMAIL", "suporte@coverde.pt")

    context = {
        'user': user,
        'activation_url': activation_url,
        'domain': domain,
        'account_type_label': account_type_label,
        'is_pending_validation': is_pending_validation,
        'support_email': support_email,
    }
    
    try:
        html_message = render_to_string('emails/activation_email.html', context)
        plain_message = strip_tags(html_message)
    except:
        pending_msg = "A sua conta está pendente de validação pela equipa COVERDE." if is_pending_validation else "Depois da confirmação, a sua conta ficará ativa."
        plain_message = f"""
    Olá {user.get_full_name() or user.username},

    Bem-vindo(a) à COVERDE.
    Tipo de conta criada: {account_type_label}

    Clique no link abaixo para confirmar o seu email:
    {activation_url}

    {pending_msg}

    Suporte: {support_email}

    Obrigado,
    Equipa COVERDE
        """
        html_message = plain_message
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@cverde.pt',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Erro ao enviar email de ativação: {str(e)}')
        return False


def send_order_confirmation_email(user, order, payment):
    """Email de confirmação da encomenda/pagamento ao cliente."""
    try:
        send_mail(
            subject=f"Pagamento confirmado - Encomenda {order.reference}",
            message=(
                f"Olá {user.get_full_name() or user.username},\n\n"
                f"Pagamento de teste aprovado com sucesso.\n"
                f"Encomenda: {order.reference}\n"
                f"Referência de pagamento: {payment.reference}\n"
                f"Total: €{order.total}\n"
                f"Estado: {order.get_status_display()}\n\n"
                "Obrigado por comprar na COVERDE."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@cverde.pt',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return True
    except Exception:
        return False


def send_new_order_notification_to_producer(producer_user, order, store):
    """Notifica o produtor sobre nova encomenda associada à sua loja."""
    if not producer_user or not producer_user.email:
        return False

    try:
        send_mail(
            subject=f"Nova encomenda na loja {store.name}",
            message=(
                "Recebeu uma nova encomenda na COVERDE.\n\n"
                f"Loja: {store.name}\n"
                f"Encomenda: {order.reference}\n"
                f"Estado: {order.get_status_display()}\n\n"
                "Aceda ao seu painel de produtor para acompanhar o processamento."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@cverde.pt',
            recipient_list=[producer_user.email],
            fail_silently=True,
        )
        return True
    except Exception:
        return False


def send_password_reset_email(user, token):
    """
    Enviar email de redefinição de palavra-passe.
    
    Args:
        user: Instância do User
        token: Token de redefinição
    """
    subject = 'Redefinir palavra-passe - Cverde'
    
    # URL de redefinição
    reset_url = f'{settings.DOMAIN}/users/reset-password/{token}/'
    
    # Contexto do email
    context = {
        'user': user,
        'reset_url': reset_url,
        'domain': settings.DOMAIN,
    }
    
    # Mensagem simples
    plain_message = f"""
Olá {user.get_full_name()},

Clique no link abaixo para redefinir a sua palavra-passe:
{reset_url}

Se não solicitou esta ação, ignore este email.

Obrigado,
Equipa Cverde
    """
    
    # Enviar email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@cverde.pt',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Erro ao enviar email de redefinição: {str(e)}')
        return False
