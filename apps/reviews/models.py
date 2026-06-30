"""
COVERDE - apps/reviews/models.py
Modelos de avaliações de produtos e produtores.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count, Q

from apps.users.models import Product, Producer


class Review(models.Model):
    """
    Avaliação feita por um cliente.

    A avaliação pode ser de:
    - um produto
    OU
    - um produtor

    Nunca deve ser dos dois ao mesmo tempo.
    """

    RATING_CHOICES = (
        (1, "⭐ 1 - Muito Mau"),
        (2, "⭐⭐ 2 - Mau"),
        (3, "⭐⭐⭐ 3 - Aceitável"),
        (4, "⭐⭐⭐⭐ 4 - Bom"),
        (5, "⭐⭐⭐⭐⭐ 5 - Excelente"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Utilizador",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name="Produto",
    )

    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name="Produtor",
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="Classificação",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Comentário",
    )

    is_approved = models.BooleanField(
        default=True,
        verbose_name="Aprovada",
        help_text="Se estiver ativo, a avaliação conta para a média pública.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criada em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizada em",
    )

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                check=(
                    Q(product__isnull=False, producer__isnull=True)
                    | Q(product__isnull=True, producer__isnull=False)
                ),
                name="review_product_or_producer_only",
            ),
            models.UniqueConstraint(
                fields=["user", "product"],
                condition=Q(product__isnull=False),
                name="unique_user_product_review",
            ),
            models.UniqueConstraint(
                fields=["user", "producer"],
                condition=Q(producer__isnull=False),
                name="unique_user_producer_review",
            ),
        ]

    def clean(self):
        """
        Garante que a avaliação é feita apenas para um alvo:
        produto OU produtor.
        """

        if self.product and self.producer:
            raise ValidationError(
                "A avaliação não pode estar associada a produto e produtor ao mesmo tempo."
            )

        if not self.product and not self.producer:
            raise ValidationError(
                "A avaliação deve estar associada a um produto ou a um produtor."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.update_target_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        producer = self.producer

        result = super().delete(*args, **kwargs)

        if product:
            self.update_product_rating(product)

        if producer:
            self.update_producer_rating(producer)

        return result

    def update_target_rating(self):
        """
        Atualiza a média de rating do produto ou produtor avaliado.
        """

        if self.product:
            self.update_product_rating(self.product)

        if self.producer:
            self.update_producer_rating(self.producer)

    @staticmethod
    def update_product_rating(product):
        """
        Atualiza rating e total_reviews do produto.
        """

        data = Review.objects.filter(
            product=product,
            is_approved=True,
        ).aggregate(
            avg_rating=Avg("rating"),
            total=Count("id"),
        )

        Product.objects.filter(pk=product.pk).update(
            rating=data["avg_rating"] or 0,
            total_reviews=data["total"] or 0,
        )

    @staticmethod
    def update_producer_rating(producer):
        """
        Atualiza rating e total_ratings do produtor.
        """

        data = Review.objects.filter(
            producer=producer,
            is_approved=True,
        ).aggregate(
            avg_rating=Avg("rating"),
            total=Count("id"),
        )

        Producer.objects.filter(pk=producer.pk).update(
            rating=data["avg_rating"] or 0,
            total_ratings=data["total"] or 0,
        )

    @property
    def target(self):
        return self.product or self.producer

    @property
    def target_type(self):
        if self.product:
            return "Produto"
        if self.producer:
            return "Produtor"
        return "Indefinido"

    def __str__(self):
        target = self.target or "Sem alvo"
        user_email = getattr(self.user, "email", self.user)
        return f"{self.target_type}: {target} - {self.rating}⭐ por {user_email}"