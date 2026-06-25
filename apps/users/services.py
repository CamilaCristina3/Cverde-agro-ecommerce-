"""
COVERDE - apps/users/services.py
Serviços de utilizadores (Portugal).
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_email(user, token):
    """
    Enviar email de ativação de conta.
    
    Args:
        user: Instância do User
        token: Token de ativação
    """
    subject = 'Confirme o seu email - Cverde'
    
    # URL de ativação
    activation_url = f'{settings.DOMAIN}/users/confirm-email/{token}/'
    
    # Contexto do email
    context = {
        'user': user,
        'activation_url': activation_url,
        'domain': settings.DOMAIN,
    }
    
    # Tentar usar template HTML, fallback para texto simples
    try:
        html_message = render_to_string('emails/activation_email.html', context)
        plain_message = strip_tags(html_message)
    except:
        plain_message = f"""
Olá {user.get_full_name()},

Clique no link abaixo para confirmar o seu email:
{activation_url}

Obrigado,
Equipa Cverde
        """
        html_message = plain_message
    
    # Enviar email
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
