import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Store(models.Model):
    """
    Loja do produtor no marketplace COVERDE.
    Cada produtor pode ter uma loja principal.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente de aprovação'
        ACTIVE = 'active', 'Ativa'
        SUSPENDED = 'suspended', 'Suspensa'
        CLOSED = 'closed', 'Fechada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producer = models.ForeignKey(
        'products.ProducerProfile',  # ProducerProfile está em apps.products.models
        on_delete=models.CASCADE,
        related_name='stores',
        verbose_name='Produtor'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_stores',
        verbose_name='Proprietário',
        null=True,
        blank=True
    )

    # ========== IDENTIDADE DA LOJA ==========
    name = models.CharField(max_length=200, verbose_name='Nome da loja')
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descrição')
    logo = models.ImageField(upload_to='stores/logos/', blank=True, null=True, verbose_name='Logótipo')
    banner = models.ImageField(upload_to='stores/banners/', blank=True, null=True, verbose_name='Banner')
    tagline = models.CharField(max_length=300, blank=True, verbose_name='Slogan')

    # ========== CONTACTO ==========
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telemóvel')  # ← Portugal
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Morada')

    # ========== LOCALIZAÇÃO (Portugal) ==========
    district = models.CharField(max_length=100, blank=True, verbose_name='Distrito')
    county = models.CharField(max_length=100, blank=True, verbose_name='Concelho')
    parish = models.CharField(max_length=100, blank=True, verbose_name='Freguesia')

    # ========== POLÍTICAS ==========
    min_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Valor mínimo de encomenda (€)'  # ← Euro
    )
    delivery_time_days = models.PositiveSmallIntegerField(
        default=3,
        verbose_name='Tempo de entrega estimado (dias)'
    )
    accepts_returns = models.BooleanField(default=True, verbose_name='Aceita devoluções')
    return_policy = models.TextField(blank=True, verbose_name='Política de devoluções')

    # ========== ESTADO ==========
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    is_active = models.BooleanField(default=True, verbose_name='Ativa')
    is_featured = models.BooleanField(default=False, verbose_name='Loja em destaque')

    # ========== MÉTRICAS ==========
    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total de vendas (€)'  # ← Euro
    )
    total_products = models.PositiveIntegerField(default=0, verbose_name='Total de produtos')
    total_orders = models.PositiveIntegerField(default=0, verbose_name='Total de encomendas')
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name='Avaliação média'
    )
    review_count = models.PositiveIntegerField(default=0, verbose_name='Número de avaliações')

    # ========== COMISSÃO ==========
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=8.00,
        verbose_name='Comissão da plataforma (%)'
    )

    # ========== AUDITORIA ==========
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Aprovada em')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_stores',
        verbose_name='Aprovada por'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} [{self.get_status_display()}]'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Store.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('stores:detail', kwargs={'slug': self.slug})

    @property
    def is_active_and_approved(self):
        return self.is_active and self.status == self.Status.ACTIVE

    @property
    def full_address(self):
        """Retorna a morada completa formatada."""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.parish:
            parts.append(f'Freguesia: {self.parish}')
        if self.county:
            parts.append(f'Concelho: {self.county}')
        if self.district:
            parts.append(f'Distrito: {self.district}')
        return ', '.join(parts) if parts else 'Morada não definida'