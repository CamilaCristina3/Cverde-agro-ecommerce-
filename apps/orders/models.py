"""
COVERDE - apps/orders/models.py
Modelos: Order, OrderItem, SellerOrder
"""

import uuid
import random
import string
from django.conf import settings
from django.db import models


class Order(models.Model):
    """Encomenda principal do cliente."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente de pagamento'
        CONFIRMED = 'confirmed', 'Confirmada'
        PROCESSING = 'processing', 'Em preparação'
        SHIPPED = 'shipped', 'Enviada'
        DELIVERED = 'delivered', 'Entregue'
        CANCELLED = 'cancelled', 'Cancelada'
        REFUNDED = 'refunded', 'Reembolsada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=20, unique=True, blank=True, verbose_name='Referência')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Cliente'
    )

    # ========== ENDEREÇO DE ENTREGA (snapshot) ==========
    delivery_name = models.CharField(max_length=200, verbose_name='Nome de entrega')
    delivery_phone = models.CharField(max_length=20, verbose_name='Telemóvel de entrega')  # ← Portugal
    delivery_street = models.CharField(max_length=300, verbose_name='Rua / Bairro')
    delivery_city = models.CharField(max_length=100, verbose_name='Cidade')
    delivery_district = models.CharField(max_length=100, verbose_name='Distrito')  # ← Portugal
    delivery_country = models.CharField(max_length=100, default='Portugal', verbose_name='País')  # ← Portugal

    # ========== VALORES ==========
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Subtotal (€)'  # ← Euro
    )
    delivery_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Taxa de entrega (€)'  # ← Euro
    )
    discount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Desconto (€)'  # ← Euro
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total (€)'  # ← Euro
    )

    # ========== ESTADO ==========
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )

    # ========== NOTAS ==========
    customer_notes = models.TextField(blank=True, verbose_name='Notas do cliente')
    admin_notes = models.TextField(blank=True, verbose_name='Notas do administrador')

    # ========== DATAS DE ESTADO ==========
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Confirmada em')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='Enviada em')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='Cancelada em')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Encomenda'
        verbose_name_plural = 'Encomendas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Encomenda #{self.reference} - {self.customer.get_full_name()}'

    def save(self, *args, **kwargs):
        if not self.reference:
            chars = string.ascii_uppercase + string.digits
            self.reference = 'COV' + ''.join(random.choices(chars, k=7))  # ← COV (mais profissional)
        super().save(*args, **kwargs)

    @property
    def full_delivery_address(self):
        """Retorna a morada completa formatada."""
        parts = []
        if self.delivery_street:
            parts.append(self.delivery_street)
        if self.delivery_city:
            parts.append(self.delivery_city)
        if self.delivery_district:
            parts.append(f'Distrito: {self.delivery_district}')
        if self.delivery_country:
            parts.append(self.delivery_country)
        return ', '.join(parts) if parts else 'Morada não definida'


class OrderItem(models.Model):
    """Item de uma encomenda (snapshot dos dados no momento da compra)."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Encomenda'
    )
    product = models.ForeignKey(
        'users.Product',  # Product está em apps.users.models
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Produto'
    )
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Loja'
    )

    # ========== SNAPSHOT DOS DADOS ==========
    product_name = models.CharField(max_length=200, verbose_name='Nome do produto')
    product_unit = models.CharField(max_length=10, verbose_name='Unidade')
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço unitário (€)'  # ← Euro
    )
    quantity = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Quantidade')
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Subtotal (€)'  # ← Euro
    )

    class Meta:
        verbose_name = 'Item de Encomenda'
        verbose_name_plural = 'Itens de Encomenda'

    def __str__(self):
        return f'{self.quantity}x {self.product_name}'


class SellerOrder(models.Model):
    """
    Sub-encomenda agrupada por loja/produtor.
    O produtor só vê a sua própria SellerOrder.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        ACCEPTED = 'accepted', 'Aceite'
        REJECTED = 'rejected', 'Recusada'
        PROCESSING = 'processing', 'Em preparação'
        SHIPPED = 'shipped', 'Enviada'
        DELIVERED = 'delivered', 'Entregue'
        CANCELLED = 'cancelled', 'Cancelada'

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='seller_orders',
        verbose_name='Encomenda'
    )
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.PROTECT,
        related_name='seller_orders',
        verbose_name='Loja'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Subtotal (€)'  # ← Euro
    )
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=8.00,
        verbose_name='Comissão (%)'
    )
    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Comissão (€)'  # ← Euro
    )
    payout_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='A receber (€)'  # ← Euro
    )
    rejection_reason = models.TextField(blank=True, verbose_name='Motivo de recusa')
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sub-Encomenda do Produtor'
        verbose_name_plural = 'Sub-Encomendas dos Produtores'
        ordering = ['-created_at']

    def __str__(self):
        return f'SellerOrder #{self.order.reference} - {self.store.name}'

    @property
    def is_accepted(self):
        return self.status == self.Status.ACCEPTED

    @property
    def is_rejected(self):
        return self.status == self.Status.REJECTED