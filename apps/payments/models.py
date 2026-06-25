"""
COVERDE - apps/payments/models.py
Modelos: Payment, ProducerPayout
NOTA: Nesta fase, todos os pagamentos são simulados (modo teste).
"""

import uuid
import random
import string
from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    Registo de pagamento.
    Em modo de desenvolvimento: todos os pagamentos são de teste.
    Campo is_test_payment=True identifica pagamentos simulados.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        PROCESSING = 'processing', 'Em processamento'
        PAID = 'paid', 'Pago'
        FAILED = 'failed', 'Falhado'
        CANCELLED = 'cancelled', 'Cancelado'
        REFUNDED = 'refunded', 'Reembolsado'
        TEST_APPROVED = 'test_approved', 'Aprovado (Teste)'

    class Method(models.TextChoices):
        # Métodos de pagamento adaptados para Portugal
        MB_WAY = 'mb_way', 'MB WAY'  # ← Portugal
        MULTIBANCO = 'multibanco', 'Referência Multibanco'  # ← Portugal
        PAYPAL = 'paypal', 'PayPal'
        CARD_TEST = 'card_test', 'Cartão Teste'
        BANK_TRANSFER_TEST = 'bank_transfer_test', 'Transferência Bancária Teste'
        CASH_ON_DELIVERY = 'cash_on_delivery', 'Pagamento na Entrega'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='Encomenda'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='Cliente',
        null=True,
        blank=True
    )

    # Referência simulada do pagamento
    reference = models.CharField(max_length=30, unique=True, blank=True, verbose_name='Referência de pagamento')

    # Método e valores
    method = models.CharField(
        max_length=30,
        choices=Method.choices,
        default=Method.CARD_TEST,
        verbose_name='Método de pagamento'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor (€)'  # ← Euro
    )

    # Estado
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )

    # MODO TESTE - campo obrigatório para identificar pagamentos simulados
    is_test_payment = models.BooleanField(
        default=True,
        verbose_name='Pagamento de teste',
        help_text='TRUE = pagamento simulado em modo de desenvolvimento. FALSE = pagamento real.'
    )

    # Dados da aprovação em modo teste
    test_password_used = models.BooleanField(default=False, verbose_name='Senha de teste usada')
    test_signature_used = models.BooleanField(default=False, verbose_name='Assinatura de teste usada')
    test_approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Aprovado (teste) em')

    # Datas reais
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Pago em')
    failed_at = models.DateTimeField(null=True, blank=True, verbose_name='Falhado em')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='Cancelado em')
    refunded_at = models.DateTimeField(null=True, blank=True, verbose_name='Reembolsado em')

    # Notas
    notes = models.TextField(blank=True, verbose_name='Notas')
    failure_reason = models.CharField(max_length=300, blank=True, verbose_name='Motivo de falha')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']

    def __str__(self):
        mode = '[TESTE]' if self.is_test_payment else '[REAL]'
        return f'Pagamento {mode} #{self.reference} - {self.amount} €'  # ← Euro

    def save(self, *args, **kwargs):
        if not self.reference:
            chars = string.ascii_uppercase + string.digits
            self.reference = 'COV-PAY-' + ''.join(random.choices(chars, k=8))  # ← COV-PAY-
        super().save(*args, **kwargs)

    def approve_test_payment(self, credential):
        """
        Aprova o pagamento em modo de teste.
        Aceita senha (1234) ou assinatura (COVERDE-TEST).
        """
        test_password = getattr(settings, 'PAYMENT_TEST_PASSWORD', '1234')
        test_signature = getattr(settings, 'PAYMENT_TEST_SIGNATURE', 'COVERDE-TEST')

        if credential == test_password:
            self.test_password_used = True
        elif credential == test_signature:
            self.test_signature_used = True
        else:
            return False, 'Credencial de teste inválida.'

        self.status = self.Status.TEST_APPROVED
        self.test_approved_at = timezone.now()
        self.paid_at = timezone.now()
        self.save()

        # Confirmar a encomenda associada
        order = self.order
        order.status = 'confirmed'
        order.confirmed_at = timezone.now()
        order.save(update_fields=['status', 'confirmed_at'])

        return True, 'Pagamento de teste aprovado com sucesso.'


class ProducerPayout(models.Model):
    """Pagamento a efetuar ao produtor pela plataforma."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        PROCESSING = 'processing', 'Em processamento'
        PAID = 'paid', 'Pago'
        FAILED = 'failed', 'Falhado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.PROTECT,
        related_name='payouts',
        verbose_name='Loja'
    )
    seller_order = models.ForeignKey(
        'orders.SellerOrder',
        on_delete=models.PROTECT,
        related_name='payouts',
        verbose_name='Sub-encomenda'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor a pagar (€)'  # ← Euro
    )
    commission_deducted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Comissão deduzida (€)'  # ← Euro
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    is_test = models.BooleanField(default=True, verbose_name='Payout de teste')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Pago em')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento ao Produtor'
        verbose_name_plural = 'Pagamentos aos Produtores'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payout {self.store.name} - {self.amount} €'  # ← Euro