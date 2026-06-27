from collections import Counter

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from apps.users.models import Producer


User = get_user_model()


def normalize_email(value):
    return (value or "").strip().lower()


def main():
    users = list(User.objects.all().order_by("id"))
    emails = [normalize_email(u.email) for u in users if normalize_email(u.email)]
    email_counts = Counter(emails)

    changed = 0
    skipped_duplicate_email = 0
    skipped_username_conflict = 0
    missing_email = 0

    for user in users:
        updates = []
        email = normalize_email(user.email)

        if not email:
            missing_email += 1
        else:
            if user.email != email:
                user.email = email
                updates.append("email")

            if email_counts[email] > 1:
                skipped_duplicate_email += 1
            else:
                username_conflict = User.objects.filter(username__iexact=email).exclude(pk=user.pk).exists()
                if username_conflict:
                    skipped_username_conflict += 1
                elif user.username != email:
                    user.username = email
                    updates.append("username")

        is_producer = Producer.objects.filter(user_id=user.pk).exists()
        if user.is_superuser:
            if getattr(user, "user_type", None) != "admin":
                user.user_type = "admin"
                updates.append("user_type")
            if not user.is_staff:
                user.is_staff = True
                updates.append("is_staff")
            if hasattr(user, "is_verified") and not user.is_verified:
                user.is_verified = True
                updates.append("is_verified")
            if hasattr(user, "email_verified_at") and not user.email_verified_at:
                user.email_verified_at = timezone.now()
                updates.append("email_verified_at")
        elif is_producer:
            if getattr(user, "user_type", None) != "producer":
                user.user_type = "producer"
                updates.append("user_type")
        else:
            if getattr(user, "user_type", None) != "consumer":
                user.user_type = "consumer"
                updates.append("user_type")

        if updates:
            with transaction.atomic():
                user.save(update_fields=list(dict.fromkeys(updates)))
            changed += 1

    summary = Counter([getattr(u, "user_type", "") or "" for u in User.objects.all()])

    mismatch_exact = 0
    for u in User.objects.exclude(email__isnull=True).exclude(email=""):
        if normalize_email(u.username) != normalize_email(u.email):
            mismatch_exact += 1

    print("=== NORMALIZACAO DE CONTAS ===")
    print("utilizadores_total=", User.objects.count())
    print("registos_alterados=", changed)
    print("missing_email=", missing_email)
    print("skipped_duplicate_email=", skipped_duplicate_email)
    print("skipped_username_conflict=", skipped_username_conflict)
    print("mismatch_username_email=", mismatch_exact)
    print("by_type=", dict(summary))

    sample_admin = list(
        User.objects.filter(user_type="admin").values(
            "id", "email", "username", "is_active", "is_staff", "is_superuser", "is_verified"
        )[:3]
    )
    sample_producer = list(
        User.objects.filter(user_type="producer").values("id", "email", "username", "is_active", "is_verified")[:3]
    )
    sample_consumer = list(
        User.objects.filter(user_type="consumer").values("id", "email", "username", "is_active", "is_verified")[:3]
    )
    print("sample_admin=", sample_admin)
    print("sample_producer=", sample_producer)
    print("sample_consumer=", sample_consumer)


if __name__ == "__main__":
    main()
