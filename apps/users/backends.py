import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.db import transaction
from django.utils import timezone

User = get_user_model()

logger = logging.getLogger(__name__)


def _client_ip(request):
    if request is None:
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _lockout_settings():
    max_attempts = int(getattr(settings, "MAX_LOGIN_ATTEMPTS", 5))
    lock_minutes = int(getattr(settings, "ACCOUNT_LOCK_MINUTES", 15))
    return max_attempts, lock_minutes


class EmailAuthBackend(ModelBackend):
    """
    Authenticate using either username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            return None

        identifier = str(username).strip()
        if not identifier:
            return None

        max_attempts, lock_minutes = _lockout_settings()
        ip = _client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT") if request is not None else None

        with transaction.atomic():
            user = (
                User.objects.select_for_update()
                .filter(email__iexact=identifier)
                .first()
            ) or (
                User.objects.select_for_update()
                .filter(username__iexact=identifier)
                .first()
            )

            if user is None:
                logger.warning("Login failed for unknown user: %s (ip=%s ua=%s)", identifier, ip, user_agent)
                return None

            locked_until = getattr(user, "locked_until", None)
            if locked_until and locked_until > timezone.now():
                logger.warning("Login blocked (locked) for user=%s (ip=%s ua=%s until=%s)", user.pk, ip, user_agent, locked_until)
                return None

            if user.check_password(password) and self.user_can_authenticate(user):
                # sucesso: reset tentativas / lock e guardar IP
                updated_fields = []
                if getattr(user, "login_attempts", 0) != 0:
                    user.login_attempts = 0
                    updated_fields.append("login_attempts")
                if getattr(user, "locked_until", None) is not None:
                    user.locked_until = None
                    updated_fields.append("locked_until")
                if ip and getattr(user, "last_login_ip", None) != ip:
                    user.last_login_ip = ip
                    updated_fields.append("last_login_ip")
                if updated_fields:
                    user.save(update_fields=updated_fields)
                return user

            # falhou: incrementar tentativas e bloquear após N tentativas
            attempts = int(getattr(user, "login_attempts", 0) or 0) + 1
            user.login_attempts = attempts
            update_fields = ["login_attempts"]
            if attempts >= max_attempts:
                user.locked_until = timezone.now() + timedelta(minutes=lock_minutes)
                update_fields.append("locked_until")
                logger.warning(
                    "Account locked after failed logins user=%s (attempts=%s ip=%s ua=%s)",
                    user.pk,
                    attempts,
                    ip,
                    user_agent,
                )
            else:
                logger.info(
                    "Login failed user=%s (attempts=%s ip=%s ua=%s)",
                    user.pk,
                    attempts,
                    ip,
                    user_agent,
                )
            user.save(update_fields=update_fields)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
