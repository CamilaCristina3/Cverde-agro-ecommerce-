"""
COVERDE - apps/reviews/models.py
Modelos de avaliações (Portugal).
"""

from django.db import models
from django.conf import settings

# ✅ Importações corrigidas
from apps.users.models import Product  # Product está em users
from apps.users_auth.models import User
from apps.products.models import ProducerProfile  # ProducerProfile está em products


class Review(models.Model):
    """Avaliação de produto ou produtor."""

    RATING_CHOICES = (
        (1, '⭐ 1 - Muito Mau'),
        (2, '⭐⭐ 2 - Mau'),
        (3, '⭐⭐⭐ 3 - Aceitável'),
        (4, '⭐⭐⭐⭐ 4 - Bom'),
        (5, '⭐⭐⭐⭐⭐ 5 - Excelente'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Utilizador'
    )

    # Avaliação de produto ou produtor (apenas um)
    product = models.ForeignKey(
        Product,  # ← agora importado corretamente
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Produto'
    )

    producer = models.ForeignKey(
        ProducerProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Produtor'
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='Classificação'
    )

    comment = models.TextField(
        blank=True,
        verbose_name='Comentário'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        target = self.product or self.producer
        return f"{target} - {self.rating}⭐ por {self.user.email}"