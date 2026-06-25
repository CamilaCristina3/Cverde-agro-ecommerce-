import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


# ========== LEGACY USER MODEL REMOVED ==========
# The legacy User model has been removed.
# Use apps.users_auth.User (which is AUTH_USER_MODEL) instead.
# This eliminates the conflicting related_name issues with Django's Group and Permission models.



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


class SupplierProfile(models.Model):
    """Perfil do produtor/fornecedor."""

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
    nif = models.CharField(max_length=20, blank=True, verbose_name='NIF')  # ← Portugal: NIF
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


class Address(models.Model):
    """Morada de entrega do utilizador."""

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
    district = models.CharField(max_length=100, verbose_name='Distrito')  # ← Portugal: Distrito
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Código Postal')  # ← Portugal
    country = models.CharField(max_length=100, default='Portugal', verbose_name='País')  # ← Portugal
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
        # Se este for marcado como padrão, remover padrão dos outros
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='Nome do produto')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Descrição')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Categoria'
    )
    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Produtor',
        limit_choices_to={'role': 'producer'}
    )

    # Preço e estoque
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço (€)')
    stock = models.PositiveIntegerField(default=0, verbose_name='Quantidade em stock')
    unit = models.CharField(
        max_length=50,
        default='kg',
        verbose_name='Unidade',
        help_text='kg, unidade, litro, etc'
    )

    # Imagem principal
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Imagem principal'
    )

    # Certificações
    is_organic = models.BooleanField(default=False, verbose_name='Biológico')
    certification = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Certificação',
        help_text='Ex: DOP, IGP, Biológico certificado'
    )

    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    is_featured = models.BooleanField(default=False, verbose_name='Em destaque')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')  # Para compatibilidade

    # Avaliação
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name='Avaliação média'
    )
    total_reviews = models.PositiveIntegerField(default=0, verbose_name='Total de avaliações')

    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['producer']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.name} - {self.producer.get_full_name()}'

    @property
    def display_price(self):
        """Preço formatado com unidade"""
        return f'{self.price:.2f}€/{self.unit}'


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