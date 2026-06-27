"""
COVERDE - apps/users/models.py
Modelos principais da aplicação COVERDE (Portugal).
"""

import uuid
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# ============================================
# 1. PERFIL DE CLIENTE
# ============================================

class CustomerProfile(models.Model):
    """Perfil alargado do cliente."""

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não dizer'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name='Utilizador'
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Data de nascimento')
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=GENDER_CHOICES,
        verbose_name='Género'
    )
    newsletter_subscribed = models.BooleanField(default=True, verbose_name='Subscrito a newsletter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Cliente'
        verbose_name_plural = 'Perfis de Clientes'

    def __str__(self):
        return f'Perfil Cliente: {self.user.get_full_name()}'


# ============================================
# 2. PERFIL DE PRODUTOR (FORNECEDOR)
# ============================================

class SupplierProfile(models.Model):
    """Perfil do produtor/fornecedor (Portugal)."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente de aprovação'
        APPROVED = 'approved', 'Aprovado'
        SUSPENDED = 'suspended', 'Suspenso'
        REJECTED = 'rejected', 'Rejeitado'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supplier_profile',
        verbose_name='Utilizador'
    )
    company_name = models.CharField(max_length=200, verbose_name='Nome da empresa/quinta')
    nif = models.CharField(max_length=20, blank=True, verbose_name='NIF')
    description = models.TextField(blank=True, verbose_name='Descrição')
    logo = models.ImageField(upload_to='suppliers/logos/', blank=True, null=True, verbose_name='Logótipo')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Telemóvel de contacto')
    contact_email = models.EmailField(blank=True, verbose_name='Email de contacto')
    address = models.TextField(blank=True, verbose_name='Morada')
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
        related_name='approved_suppliers',
        verbose_name='Aprovado por'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Produtor'
        verbose_name_plural = 'Perfis de Produtores'

    def __str__(self):
        return f'{self.company_name} ({self.user.email})'


# ============================================
# 3. PRODUTOR (PRODUCER) - MODELO PRINCIPAL
# ============================================

class Producer(models.Model):
    """
    Produtor agrícola (tabela: users_producer).
    Relaciona-se com User via OneToOneField.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente de aprovação'
        APPROVED = 'approved', 'Aprovado'
        SUSPENDED = 'suspended', 'Suspenso'
        REJECTED = 'rejected', 'Rejeitado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='producer',
        verbose_name='Utilizador'
    )

    # Dados do produtor
    name = models.CharField(max_length=200, verbose_name='Nome da quinta/empresa')
    description = models.TextField(blank=True, verbose_name='Descrição')
    location = models.CharField(max_length=200, blank=True, verbose_name='Localização')

    # Documentação (Portugal)
    nif = models.CharField(max_length=20, blank=True, verbose_name='NIF')
    verification_document = models.FileField(
        upload_to='producers/verification/',
        blank=True,
        null=True,
        verbose_name='Documento de verificação'
    )

    # Estado
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    is_verified = models.BooleanField(default=False, verbose_name='Verificado')
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='Verificado em')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_producers',
        verbose_name='Verificado por'
    )
    rejection_reason = models.TextField(blank=True, verbose_name='Motivo da rejeição')

    # Métricas
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_ratings = models.PositiveIntegerField(default=0, verbose_name='Total de avaliações')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Total de produtos')
    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total de vendas (€)'
    )

    # Auditoria
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Eliminado em')

    class Meta:
        db_table = 'users_producer'
        verbose_name = 'Produtor'
        verbose_name_plural = 'Produtores'
        ordering = ['-rating', '-total_sales']

    def __str__(self):
        return f'{self.name} - {self.user.get_full_name() or self.user.email}'

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED

    def approve(self, admin_user):
        """Aprovar produtor."""
        self.status = self.Status.APPROVED
        self.is_verified = True
        self.verified_at = timezone.now()
        self.verified_by = admin_user
        self.save(update_fields=['status', 'is_verified', 'verified_at', 'verified_by'])

    def suspend(self):
        """Suspender produtor."""
        self.status = self.Status.SUSPENDED
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])

    def reject(self, reason=''):
        """Rejeitar produtor com motivo."""
        self.status = self.Status.REJECTED
        self.rejection_reason = reason
        self.is_active = False
        self.save(update_fields=['status', 'rejection_reason', 'is_active'])

    def soft_delete(self):
        """Eliminação suave."""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['deleted_at', 'is_active'])


# ============================================
# 4. MORADA
# ============================================

class Address(models.Model):
    """Morada de entrega do utilizador (Portugal)."""

    class AddressType(models.TextChoices):
        HOME = 'home', 'Casa'
        WORK = 'work', 'Trabalho'
        OTHER = 'other', 'Outro'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Utilizador'
    )
    label = models.CharField(
        max_length=20,
        choices=AddressType.choices,
        default=AddressType.HOME,
        verbose_name='Tipo'
    )
    full_name = models.CharField(max_length=200, verbose_name='Nome completo')
    phone = models.CharField(max_length=20, verbose_name='Telemóvel')
    street = models.CharField(max_length=300, verbose_name='Rua / Bairro')
    city = models.CharField(max_length=100, verbose_name='Cidade')
    district = models.CharField(max_length=100, verbose_name='Distrito')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Código Postal')
    country = models.CharField(max_length=100, default='Portugal', verbose_name='País')
    is_default = models.BooleanField(default=False, verbose_name='Morada padrão')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Morada'
        verbose_name_plural = 'Moradas'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.street}, {self.city}'

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


# ============================================
# 5. TOKEN DE ATIVAÇÃO DE CONTA
# ============================================

class AccountActivationToken(models.Model):
    """
    Token de ativação de conta enviado por email.
    Tem validade configurável em settings.ACCOUNT_ACTIVATION_TOKEN_HOURS.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activation_tokens',
        verbose_name='Utilizador'
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Token')
    is_used = models.BooleanField(default=False, verbose_name='Usado')
    expires_at = models.DateTimeField(verbose_name='Expira em')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token de Ativação'
        verbose_name_plural = 'Tokens de Ativação'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            hours = getattr(settings, 'ACCOUNT_ACTIVATION_TOKEN_HOURS', 48)
            self.expires_at = timezone.now() + timedelta(hours=hours)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Token {self.token} - {self.user.email}'

    @property
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])


# ============================================
# 6. NOTIFICAÇÃO
# ============================================

class Notification(models.Model):
    """Notificações internas do sistema."""

    class NotifType(models.TextChoices):
        ORDER_NEW = 'order_new', 'Nova encomenda'
        ORDER_CONFIRMED = 'order_confirmed', 'Encomenda confirmada'
        PAYMENT_APPROVED = 'payment_approved', 'Pagamento aprovado'
        ACCOUNT_APPROVED = 'account_approved', 'Conta aprovada'
        ACCOUNT_REJECTED = 'account_rejected', 'Conta rejeitada'
        PRODUCT_APPROVED = 'product_approved', 'Produto aprovado'
        GENERAL = 'general', 'Geral'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilizador'
    )
    notif_type = models.CharField(
        max_length=30,
        choices=NotifType.choices,
        default=NotifType.GENERAL,
        verbose_name='Tipo'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensagem')
    is_read = models.BooleanField(default=False, verbose_name='Lida')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user.email}'


# ============================================
# 7. CATEGORIA
# ============================================

class Category(models.Model):
    """Categorias de produtos (Portugal)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descrição')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Categoria pai'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Ícone',
        help_text='Classe FontAwesome, ex: fa-apple-alt'
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )
    is_active = models.BooleanField(default=True, verbose_name='Ativa')
    ordering = models.PositiveIntegerField(default=0, verbose_name='Ordem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordering', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ============================================
# 8. PRODUTO
# ============================================

class Product(models.Model):
    """
    Modelo de Produto do COVERDE (Portugal).
    Cada produto pertence a um produtor.
    """

    STATUS_CHOICES = (
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('discontinued', 'Descontinuado'),
    )

    UNIT_CHOICES = (
        ('kg', 'Quilograma'),
        ('un', 'Unidade'),
        ('l', 'Litro'),
        ('pct', 'Pacote'),
        ('maco', 'Maço'),
        ('caixa', 'Caixa'),
        ('dúzia', 'Dúzia'),
    )

    CERTIFICATION_CHOICES = (
        ('', 'Sem certificação'),
        ('biologico', 'Biológico'),
        ('dop', 'DOP'),
        ('igp', 'IGP'),
        ('integrada', 'Produção Integrada'),
        ('tradicional', 'Produto Tradicional'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='Nome do produto')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Descrição')

    # Relacionamentos
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Categoria'
    )
    producer = models.ForeignKey(
        Producer,  # ← Agora referência o modelo Producer
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Produtor'
    )

    # Preço e estoque
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Preço (€)'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Quantidade em stock')
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='kg',
        verbose_name='Unidade'
    )

    # Certificação
    certification = models.CharField(
        max_length=50,
        choices=CERTIFICATION_CHOICES,
        blank=True,
        verbose_name='Certificação'
    )

    # Imagem principal
    main_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Imagem principal'
    )
    extra_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Imagens adicionais'
    )

    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    is_featured = models.BooleanField(default=False, verbose_name='Em destaque')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    # Métricas
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name='Avaliação média'
    )
    total_reviews = models.PositiveIntegerField(default=0, verbose_name='Total de avaliações')
    total_sold = models.PositiveIntegerField(default=0, verbose_name='Total vendido')

    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_product'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['producer']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.name} - {self.producer.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_price(self):
        """Preço formatado com unidade."""
        return f'{self.price:.2f} €/{self.unit}'
