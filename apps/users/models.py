from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model extendable for producers/consumers."""

    pass
