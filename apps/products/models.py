import uuid
import re
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_portuguese_nif(value):
    """
    Validação simples para NIF português (9 dígitos).
    """
    if not value:
        return
    # Remover espaços e hífens
    nif = re.sub(r'[-\s]', '', value)
    if not nif.isdigit() or len(nif) != 9:
        raise ValidationError('O NIF deve ter 9 dígitos numéricos.')
    # Verificar se começa com dígito válido (1,2,3,5,6,8,9)
    if nif[0] not in '1235689':
        raise ValidationError('NIF inválido. Deve começar com 1,2,3,5,6,8 ou 9.')


class ProducerProfile(models.Model):
    """
    Perfil do produtor agrícola (Portugal).
    Um produtor pode ter uma ou mais lojas.
    Precisa de aprovação do administrador para vender.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente de aprovação'
        APPROVED = 'approved', 'Aprovado'
        SUSPENDED = 'suspended', 'Suspenso'
        REJECTED = 'rejected', 'Rejeitado'

    class ProducerType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Produtor Individual'
        COOPERATIVE = 'cooperative', 'Cooperativa'
        COMPANY = 'company', 'Empresa Agrícola'
        ASSOCIATION = 'association', 'Associação'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='producer_profile',
        verbose_name='Utilizador'
    )

    # ========== INFORMAÇÃO DO PRODUTOR ==========
    producer_type = models.CharField(
        max_length=20,
        choices=ProducerType.choices,
        default=ProducerType.INDIVIDUAL,
        verbose_name='Tipo de produtor'
    )
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome da empresa / cooperativa'
    )
    nif = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_portuguese_nif],
        verbose_name='NIF',
        help_text='Número de Identificação Fiscal (Portugal) - 9 dígitos'
    )
    bio = models.TextField(blank=True, verbose_name='Sobre o produtor')
    logo = models.ImageField(
        upload_to='producers/logos/',
        blank=True,
        null=True,
        verbose_name='Logótipo'
    )
    banner = models.ImageField(
        upload_to='producers/banners/',
        blank=True,
        null=True,
        verbose_name='Banner'
    )

    # ========== LOCALIZAÇÃO DA EXPLORAÇÃO (Portugal) ==========
    farm_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome da exploração'
    )
    farm_address = models.TextField(blank=True, verbose_name='Morada da exploração')
    district = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Distrito'
    )
    county = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Concelho'
    )
    parish = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Freguesia'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Código Postal',
        help_text='Ex: 3000-000'
    )

    # ========== CONTACTO ==========
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telemóvel de contacto'
    )
    contact_email = models.EmailField(blank=True, verbose_name='Email de contacto')
    website = models.URLField(blank=True, verbose_name='Website')

    # ========== DADOS BANCÁRIOS ==========
    bank_name = models.CharField(max_length=100, blank=True, verbose_name='Banco')
    bank_account = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='IBAN',
        help_text='Número de conta bancária (IBAN)'
    )
    bank_owner = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Titular da conta'
    )

    # ========== ESTADO E APROVAÇÃO ==========
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Aprovado em')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_producers',
        verbose_name='Aprovado por'
    )
    rejection_reason = models.TextField(blank=True, verbose_name='Motivo de rejeição')
    rejected_at = models.DateTimeField(null=True, blank=True, verbose_name='Rejeitado em')  # ← Adicionado
    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rejected_producers',
        verbose_name='Rejeitado por'
    )

    # ========== COMISSÃO ==========
    custom_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Comissão personalizada (%)',
        help_text='Deixar vazio para usar a comissão padrão da plataforma'
    )

    # ========== MÉTRICAS ==========
    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total de vendas (€)'
    )
    total_orders = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de encomendas'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name='Avaliação média'
    )
    total_reviews = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de avaliações'
    )

    # ========== AUDITORIA ==========
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Eliminado em')

    class Meta:
        verbose_name = 'Perfil de Produtor'
        verbose_name_plural = 'Perfis de Produtores'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        name = self.company_name or self.user.get_full_name()
        return f'{name} [{self.get_status_display()}]'

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED

    @property
    def is_pending(self):
        return self.status == self.Status.PENDING

    @property
    def is_rejected(self):
        return self.status == self.Status.REJECTED

    @property
    def is_suspended(self):
        return self.status == self.Status.SUSPENDED

    @property
    def display_name(self):
        return self.company_name or self.user.get_full_name()

    @property
    def is_active_and_approved(self):
        return self.is_active and self.is_approved

    @property
    def full_location(self):
        """Retorna a localização completa formatada (Portugal)."""
        parts = []
        if self.farm_name:
            parts.append(self.farm_name)
        if self.parish:
            parts.append(f'Freguesia: {self.parish}')
        if self.county:
            parts.append(f'Concelho: {self.county}')
        if self.district:
            parts.append(f'Distrito: {self.district}')
        if self.postal_code:
            parts.append(f'CP: {self.postal_code}')
        return ', '.join(parts) if parts else 'Localização não definida'

    def approve(self, admin_user):
        """Aprovar produtor e ativar a sua conta (Portugal)."""
        self.status = self.Status.APPROVED
        self.approved_at = timezone.now()
        self.approved_by = admin_user
        self.save(update_fields=['status', 'approved_at', 'approved_by'])

        # Atualizar status do utilizador (se tiver o campo)
        if hasattr(self.user, 'status'):
            try:
                self.user.status = self.user.Status.ACTIVE
                self.user.save(update_fields=['status'])
            except AttributeError:
                # Caso o User não tenha o campo 'status'
                pass

    def reject(self, admin_user, reason=''):
        """Rejeitar produtor com motivo (Portugal)."""
        self.status = self.Status.REJECTED
        self.rejection_reason = reason
        self.rejected_at = timezone.now()
        self.rejected_by = admin_user
        self.is_active = False
        self.save(update_fields=['status', 'rejection_reason', 'rejected_at', 'rejected_by', 'is_active'])

    def suspend(self):
        """Suspender produtor (Portugal)."""
        self.status = self.Status.SUSPENDED
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])

    def reactivate(self):
        """Reativar produtor suspenso (Portugal)."""
        self.status = self.Status.APPROVED
        self.is_active = True
        self.save(update_fields=['status', 'is_active'])

    def soft_delete(self):
        """Eliminação suave - não remove dados reais (Portugal)."""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['deleted_at', 'is_active'])

    def update_metrics(self):
        """Atualizar métricas do produtor (Portugal)."""
        self.total_orders = self.user.orders.count() if hasattr(self.user, 'orders') else 0
        # Atualizar avaliação média
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(r.rating for r in reviews) / reviews.count()
            self.total_reviews = reviews.count()
        self.save()