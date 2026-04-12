"""
Modelos do Coverde - Autenticação, Utilizadores, Produtores, Produtos, Encomendas, Pagamentos e Notificações
Todos os modelos centralizados para facilitar a manutenção e evitar importações circulares
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta


# ============================================
# 1. MÓDULO DE AUTENTICAÇÃO E UTILIZADORES (Users)
# ============================================

class User(AbstractUser):
    """
    Modelo de utilizador personalizado para Coverde.
    Suporta diferentes tipos de perfis (consumidor, produtor, administrador)
    """
    
    USER_TYPE_CHOICES = (
        ('consumer', 'Consumidor'),
        ('producer', 'Produtor'),
        ('admin', 'Administrador'),
    )
    
    # Dados básicos
    user_type = models.CharField(
        'Tipo de utilizador',
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='consumer'
    )
    
    phone = models.CharField(
        'Telemóvel',
        max_length=15,
        validators=[
            RegexValidator(
                r"^\+?\d{9,15}$",
                "Número de telemóvel inválido. Use apenas dígitos, com ou sem prefixo (ex.: 912345678 ou +351912345678).",
            )
        ],
        help_text="Apenas dígitos, com ou sem prefixo (ex.: 912345678 ou +351912345678).",
        blank=True
    )
    
    # Localização (Portugal)
    district = models.CharField('Distrito', max_length=100, blank=True)
    county = models.CharField('Concelho', max_length=100, blank=True)
    parish = models.CharField('Freguesia', max_length=100, blank=True)
    
    # Verificação e status
    is_verified = models.BooleanField('Conta verificada', default=False)
    email_verified_at = models.DateTimeField('Email verificado em', null=True, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    # Imagem de perfil
    profile_image = models.ImageField(
        'Imagem de perfil',
        upload_to='profiles/',
        blank=True,
        null=True
    )
    
    # ========== CONSENTIMENTOS RGPD ==========
    accepted_terms_at = models.DateTimeField('Aceitação dos termos', null=True, blank=True)
    accepted_privacy_policy_at = models.DateTimeField('Aceitação da política de privacidade', null=True, blank=True)
    marketing_opt_in = models.BooleanField('Aceita marketing', default=False)
    marketing_opt_in_at = models.DateTimeField('Data de aceitação de marketing', null=True, blank=True)
    producer_public_profile_consent_at = models.DateTimeField('Consentimento perfil público', null=True, blank=True)
    
    # ========== RGPD - DIREITO AO ESQUECIMENTO ==========
    data_exported_at = models.DateTimeField('Última exportação de dados', null=True, blank=True)
    data_deleted_at = models.DateTimeField('Data de eliminação da conta', null=True, blank=True)
    deletion_requested_at = models.DateTimeField('Pedido de eliminação', null=True, blank=True)
    
    # ========== SEGURANÇA ==========
    login_attempts = models.IntegerField('Tentativas de login', default=0)
    locked_until = models.DateTimeField('Bloqueado até', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField('Último IP de login', null=True, blank=True)
    two_factor_enabled = models.BooleanField('2FA por email', default=False)
    
    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"
    
    def is_producer(self):
        return self.user_type == 'producer'
    
    def is_consumer(self):
        return self.user_type == 'consumer'
    
    def is_admin_user(self):
        return self.user_type == 'admin' or self.is_superuser
    
    def delete_account(self):
        """Direito ao esquecimento - anonimizar dados"""
        self.username = f"deleted_user_{self.id}_{uuid.uuid4().hex[:8]}"
        self.email = f"deleted_{self.id}@deleted.coverde.pt"
        self.first_name = "Utilizador"
        self.last_name = "Eliminado"
        self.phone = ""
        self.district = ""
        self.county = ""
        self.parish = ""
        self.profile_image = None
        self.is_active = False
        self.data_deleted_at = timezone.now()
        self.save()
    
    def export_personal_data(self):
        """Portabilidade de dados - exportar em JSON"""
        return {
            'personal_data': {
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone': self.phone,
                'district': self.district,
                'county': self.county,
                'parish': self.parish,
                'date_joined': self.date_joined.isoformat() if self.date_joined else None,
                'last_login': self.last_login.isoformat() if self.last_login else None,
            },
            'consents': {
                'terms_accepted_at': self.accepted_terms_at.isoformat() if self.accepted_terms_at else None,
                'privacy_accepted_at': self.accepted_privacy_policy_at.isoformat() if self.accepted_privacy_policy_at else None,
                'marketing_opt_in': self.marketing_opt_in,
                'marketing_opt_in_at': self.marketing_opt_in_at.isoformat() if self.marketing_opt_in_at else None,
            },
            'statistics': {
                'total_orders': self.orders.count(),
                'total_spent': sum(order.total for order in self.orders.all()),
                'total_reviews': self.reviews.count(),
            }
        }


# ============================================
# 2. MÓDULO DE PRODUTORES (Producers)
# ============================================

class Producer(models.Model):
    """Perfil de produtor agrícola"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='producer',
        verbose_name='Utilizador'
    )
    
    # Dados do produtor
    name = models.CharField('Nome da quinta/empresa', max_length=200)
    description = models.TextField('Descrição', blank=True)
    location = models.CharField('Localização', max_length=200, blank=True)
    
    # Documentação e verificação
    nif = models.CharField('NIF', max_length=20, blank=True)
    verification_document = models.FileField(
        'Documento de verificação',
        upload_to='producers/verification/',
        blank=True,
        null=True
    )
    is_verified = models.BooleanField('Verificado', default=False)
    verified_at = models.DateTimeField('Verificado em', null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_producers',
        verbose_name='Verificado por'
    )
    
    # Métricas
    rating = models.DecimalField(
        'Avaliação',
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_ratings = models.IntegerField('Total de avaliações', default=0)
    total_products = models.IntegerField('Total de produtos', default=0)
    total_sales = models.IntegerField('Total de vendas', default=0)
    
    # Status
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Produtor'
        verbose_name_plural = 'Produtores'
        ordering = ['-rating', '-total_sales']

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name() or self.user.username}"

    def clean(self):
        super().clean()
        if self.user_id and getattr(self.user, "user_type", None) != "producer":
            raise ValidationError({"user": "O utilizador associado deve ter user_type='producer'."})
    
    def update_metrics(self):
        """Atualizar métricas do produtor"""
        self.total_products = self.products.filter(is_active=True).count()
        # total_sales e rating são atualizados via signals
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


# ============================================
# 3. MÓDULO DE PRODUTOS (Products)
# ============================================

class Category(models.Model):
    """Categoria de produtos"""
    
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Categoria pai'
    )
    icon = models.CharField('Ícone', max_length=50, blank=True)
    image = models.ImageField('Imagem', upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField('Ativo', default=True)
    order = models.IntegerField('Ordem', default=0)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Produto agrícola"""
    
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
        ('dop', 'DOP - Denominação de Origem Protegida'),
        ('igp', 'IGP - Indicação Geográfica Protegida'),
        ('integrada', 'Produção Integrada'),
        ('tradicional', 'Produto Tradicional'),
    )
    
    # Relacionamentos
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Produtor'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Categoria'
    )
    
    # Dados básicos
    name = models.CharField('Nome do produto', max_length=200)
    slug = models.SlugField('Slug', unique=True, blank=True)
    description = models.TextField('Descrição', blank=True)
    
    # Preço e stock
    price = models.DecimalField(
        'Preço (€)',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    stock = models.PositiveIntegerField('Stock', default=0)
    unit = models.CharField('Unidade', max_length=20, choices=UNIT_CHOICES, default='kg')
    
    # Certificação
    certification = models.CharField(
        'Certificação',
        max_length=50,
        choices=CERTIFICATION_CHOICES,
        blank=True
    )
    
    # Imagens
    main_image = models.ImageField('Imagem principal', upload_to='products/')
    extra_images = models.JSONField('Imagens adicionais', default=list, blank=True)
    
    # Métricas
    average_rating = models.DecimalField(
        'Avaliação média',
        max_digits=3,
        decimal_places=2,
        default=0
    )
    total_reviews = models.PositiveIntegerField('Total de avaliações', default=0)
    total_sold = models.PositiveIntegerField('Total vendido', default=0)
    
    # Status
    is_active = models.BooleanField('Ativo para venda', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.producer.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def update_rating(self):
        """Atualizar avaliação média do produto"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = sum(r.rating for r in reviews) / reviews.count()
            self.total_reviews = reviews.count()
        else:
            self.average_rating = 0
            self.total_reviews = 0
        self.save()


# ============================================
# 4. MÓDULO DE ENCOMENDAS (Orders)
# ============================================

class Order(models.Model):
    """Encomenda"""
    
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmada'),
        ('paid', 'Paga'),
        ('preparing', 'Em preparação'),
        ('shipped', 'Enviada'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelada'),
    )
    
    # Relacionamentos
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Consumidor'
    )
    
    # Valores
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField('Portes', max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField('IVA', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Entrega
    shipping_address = models.TextField('Morada de entrega')
    shipping_contact = models.CharField('Contacto de entrega', max_length=15)
    tracking_code = models.CharField('Código de rastreio', max_length=100, blank=True)
    
    # Faturação
    invoice_number = models.CharField('Número da fatura', max_length=50, blank=True)
    invoice_pdf = models.FileField('Fatura PDF', upload_to='invoices/', blank=True, null=True)
    
    # Datas
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    paid_at = models.DateTimeField('Pago em', null=True, blank=True)
    delivered_at = models.DateTimeField('Entregue em', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Encomenda'
        verbose_name_plural = 'Encomendas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Encomenda #{self.id} - {self.user.email} - {self.total}€"
    
    def generate_invoice_number(self):
        """Gerar número de fatura sequencial"""
        year = self.created_at.year
        count = Order.objects.filter(created_at__year=year).count() + 1
        self.invoice_number = f"COV-{year}-{count:06d}"
        self.save()


class OrderItem(models.Model):
    """Item de encomenda"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Encomenda'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Produto'
    )
    
    quantity = models.PositiveIntegerField(
        'Quantidade',
        default=1,
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        'Preço unitário',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    
    product_name = models.CharField('Nome do produto (cópia)', max_length=200, blank=True)
    producer_name = models.CharField('Nome do produtor (cópia)', max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Item da encomenda'
        verbose_name_plural = 'Itens da encomenda'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} - {self.order.id}"
    
    @property
    def total(self):
        return self.quantity * self.price


# ============================================
# 5. MÓDULO DE PAGAMENTOS (Payments)
# ============================================

class Payment(models.Model):
    """Registo de pagamento"""
    
    PAYMENT_METHOD_CHOICES = (
        ('mbway', 'MB WAY'),
        ('multibanco', 'Referência Multibanco'),
        ('paypal', 'PayPal'),
        ('card', 'Cartão de Crédito/Débito'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('failed', 'Falhado'),
        ('refunded', 'Reembolsado'),
        ('cancelled', 'Cancelado'),
    )
    
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Encomenda'
    )
    
    # Dados do pagamento
    method = models.CharField('Método', max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField('Montante', max_digits=10, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Referências externas
    transaction_id = models.CharField('ID da transação', max_length=100, blank=True)
    reference = models.CharField('Referência', max_length=100, blank=True)
    entity = models.CharField('Entidade', max_length=10, blank=True)
    
    # Dados do cliente (anonimizados para segurança)
    card_last4 = models.CharField('Últimos 4 dígitos', max_length=4, blank=True)
    card_brand = models.CharField('Bandeira', max_length=20, blank=True)
    
    # Datas
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    paid_at = models.DateTimeField('Pago em', null=True, blank=True)
    
    # Webhook
    webhook_received_at = models.DateTimeField('Webhook recebido em', null=True, blank=True)
    webhook_data = models.JSONField('Dados do webhook', default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pagamento #{self.id} - {self.order.id} - {self.amount}€ - {self.status}"


# ============================================
# 6. MÓDULO DE NOTIFICAÇÕES (Notifications)
# ============================================

class Notification(models.Model):
    """Notificação para utilizadores"""
    
    NOTIFICATION_TYPES = (
        ('order', 'Encomenda'),
        ('payment', 'Pagamento'),
        ('shipping', 'Envio'),
        ('message', 'Mensagem'),
        ('review', 'Avaliação'),
        ('promotion', 'Promoção'),
        ('alert', 'Alerta'),
        ('system', 'Sistema'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilizador'
    )
    
    notification_type = models.CharField('Tipo', max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField('Título', max_length=200)
    message = models.TextField('Mensagem')
    
    # Link para ação
    link = models.CharField('Link', max_length=500, blank=True)
    
    # Status
    is_read = models.BooleanField('Lida', default=False)
    read_at = models.DateTimeField('Lida em', null=True, blank=True)
    
    # Prioridade
    priority = models.IntegerField('Prioridade', default=0)  # 0=normal, 1=alta, 2=urgente
    
    # Datas
    created_at = models.DateTimeField('Criada em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email} - {'Lida' if self.is_read else 'Não lida'}"


class NotificationPreference(models.Model):
    """Preferências de notificação do utilizador"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name='Utilizador'
    )
    
    # Canais
    email_enabled = models.BooleanField('Notificações por email', default=True)
    push_enabled = models.BooleanField('Notificações push', default=True)
    sms_enabled = models.BooleanField('Notificações por SMS', default=False)
    
    # Tipos de notificação
    order_updates = models.BooleanField('Atualizações de encomendas', default=True)
    payment_updates = models.BooleanField('Atualizações de pagamentos', default=True)
    shipping_updates = models.BooleanField('Atualizações de envios', default=True)
    marketing_emails = models.BooleanField('Emails de marketing', default=False)
    promotions = models.BooleanField('Promoções e ofertas', default=False)
    
    # Preferências de frequência
    email_digest_frequency = models.CharField(
        'Frequência do resumo',
        max_length=20,
        choices=(
            ('instant', 'Instantâneo'),
            ('daily', 'Diário'),
            ('weekly', 'Semanal'),
        ),
        default='instant'
    )
    
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Preferência de notificação'
        verbose_name_plural = 'Preferências de notificações'
    
    def __str__(self):
        return f"Preferências de {self.user.email}"


# ============================================
# 7. MÓDULO DE AVALIAÇÕES (Reviews)
# ============================================

class Review(models.Model):
    """Avaliação de produto ou produtor"""
    
    REVIEW_TYPE_CHOICES = (
        ('product', 'Produto'),
        ('producer', 'Produtor'),
    )
    
    # Utilizador que fez a avaliação
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Consumidor'
    )
    
    review_type = models.CharField('Tipo de avaliação', max_length=20, choices=REVIEW_TYPE_CHOICES)
    
    # Produto (se avaliar produto)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Produto'
    )
    
    # Produtor (se avaliar produtor)
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Produtor'
    )
    
    # Avaliação
    rating = models.IntegerField(
        'Classificação',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Comentário', blank=True)
    
    # Encomenda associada (opcional)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Encomenda'
    )
    
    # Moderação
    is_approved = models.BooleanField('Aprovada', default=True)
    is_reported = models.BooleanField('Denunciada', default=False)
    report_reason = models.TextField('Motivo da denúncia', blank=True)
    
    # Datas
    created_at = models.DateTimeField('Criada em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizada em', auto_now=True)
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']
        unique_together = [['user', 'product'], ['user', 'producer']]
    
    def __str__(self):
        if self.product:
            return f"{self.user.email} avaliou {self.product.name} com {self.rating}★"
        elif self.producer:
            return f"{self.user.email} avaliou {self.producer.name} com {self.rating}★"
        return f"{self.user.email} deu {self.rating}★"

    def clean(self):
        """
        Regras DER/SRS:
        - rating de 1 a 5 (validators)
        - se review_type='product' => product obrigatório e producer vazio
        - se review_type='producer' => producer obrigatório e product vazio
        - consumidor só pode avaliar produtos que comprou (após entrega)
        """
        super().clean()

        if self.user and getattr(self.user, "user_type", None) not in (None, "consumer"):
            raise ValidationError({"user": "Apenas consumidores podem criar avaliações."})

        if self.review_type == "product":
            if not self.product:
                raise ValidationError({"product": "Este campo é obrigatório para avaliação de produto."})
            if self.producer:
                raise ValidationError({"producer": "Não deve selecionar um produtor para avaliação de produto."})

            if self.order:
                if self.order.user_id != self.user_id:
                    raise ValidationError({"order": "A encomenda indicada não pertence a este utilizador."})
                if self.order.status != "delivered":
                    raise ValidationError({"order": "Só pode avaliar após a encomenda estar como 'Entregue'."})
                if not OrderItem.objects.filter(order=self.order, product=self.product).exists():
                    raise ValidationError({"product": "Este produto não faz parte da encomenda indicada."})
            else:
                purchased = OrderItem.objects.filter(
                    order__user_id=self.user_id,
                    order__status="delivered",
                    product_id=self.product_id,
                ).exists()
                if not purchased:
                    raise ValidationError({"product": "Só pode avaliar produtos que comprou (após entrega)."})

        elif self.review_type == "producer":
            if not self.producer:
                raise ValidationError({"producer": "Este campo é obrigatório para avaliação de produtor."})
            if self.product:
                raise ValidationError({"product": "Não deve selecionar um produto para avaliação de produtor."})

            if self.order:
                if self.order.user_id != self.user_id:
                    raise ValidationError({"order": "A encomenda indicada não pertence a este utilizador."})
                if self.order.status != "delivered":
                    raise ValidationError({"order": "Só pode avaliar após a encomenda estar como 'Entregue'."})
                producer_in_order = OrderItem.objects.filter(
                    order=self.order,
                    product__producer_id=self.producer_id,
                ).exists()
                if not producer_in_order:
                    raise ValidationError({"producer": "Este produtor não está associado à encomenda indicada."})
            else:
                purchased = OrderItem.objects.filter(
                    order__user_id=self.user_id,
                    order__status="delivered",
                    product__producer_id=self.producer_id,
                ).exists()
                if not purchased:
                    raise ValidationError({"producer": "Só pode avaliar produtores de encomendas entregues."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Atualizar rating do produto ou produtor
        if self.product:
            self.product.update_rating()
        elif self.producer:
            reviews = self.producer.reviews.filter(is_approved=True)
            if reviews.exists():
                avg = sum(r.rating for r in reviews) / reviews.count()
                self.producer.rating = avg
                self.producer.total_ratings = reviews.count()
                self.producer.save()


# ============================================
# 8. MÓDULO DE CARRINHO (Cart) - Opcional
# ============================================

class Cart(models.Model):
    """Carrinho de compras para utilizadores não autenticados (sessão)"""
    
    session_key = models.CharField('Chave de sessão', max_length=40, unique=True)
    items = models.JSONField('Itens', default=list, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'
    
    def __str__(self):
        return f"Carrinho {self.session_key} - {len(self.items)} itens"
    
    def add_item(self, product_id, quantity=1):
        """Adicionar item ao carrinho"""
        items = self.items
        for item in items:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                break
        else:
            items.append({'product_id': product_id, 'quantity': quantity})
        self.items = items
        self.save()
    
    def remove_item(self, product_id):
        """Remover item do carrinho"""
        items = [item for item in self.items if item['product_id'] != product_id]
        self.items = items
        self.save()
    
    def clear(self):
        """Esvaziar carrinho"""
        self.items = []
        self.save()


# ============================================
# 9. MÓDULO DE REGISTO DE CONSENTIMENTOS RGPD
# ============================================

class ConsentLog(models.Model):
    """Registo de consentimentos RGPD"""
    
    CONSENT_TYPES = (
        ('cookies', 'Cookies'),
        ('terms', 'Termos e Condições'),
        ('privacy', 'Política de Privacidade'),
        ('marketing', 'Marketing'),
        ('profile_public', 'Perfil Público'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consents',
        verbose_name='Utilizador'
    )
    
    consent_type = models.CharField('Tipo de consentimento', max_length=50, choices=CONSENT_TYPES)
    status = models.CharField('Estado', max_length=20)  # 'accepted', 'rejected', 'withdrawn'
    
    # Metadados
    ip_address = models.GenericIPAddressField('Endereço IP')
    user_agent = models.TextField('User Agent')
    
    # Versão dos documentos no momento do consentimento
    document_version = models.CharField('Versão do documento', max_length=20, blank=True)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registo de consentimento'
        verbose_name_plural = 'Registos de consentimento'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.consent_type} - {self.status} - {self.created_at.date()}"


# ============================================
# 10. VERIFICAÇÃO DE EMAIL (RF02)
# ============================================

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
        verbose_name="Utilizador",
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    used_at = models.DateTimeField("Usado em", null=True, blank=True)

    class Meta:
        verbose_name = "Token de verificação de email"
        verbose_name_plural = "Tokens de verificação de email"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.created_at.date()} - {'usado' if self.used_at else 'pendente'}"


# ============================================
# 11. 2FA POR EMAIL (RF04)
# ============================================

class TwoFactorCode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="two_factor_codes",
        verbose_name="Utilizador",
    )
    code_hash = models.CharField(max_length=128, verbose_name="Hash do código")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    expires_at = models.DateTimeField("Expira em")
    used_at = models.DateTimeField("Usado em", null=True, blank=True)

    class Meta:
        verbose_name = "Código 2FA"
        verbose_name_plural = "Códigos 2FA"
        ordering = ["-created_at"]

    def __str__(self):
        return f"2FA {self.user.email} - {'usado' if self.used_at else 'pendente'}"

    @classmethod
    def issue(cls, user, code, ttl_seconds=600):
        return cls.objects.create(
            user=user,
            code_hash=make_password(code),
            expires_at=timezone.now() + timedelta(seconds=ttl_seconds),
        )

    def verify(self, code):
        if self.used_at:
            return False
        if self.expires_at < timezone.now():
            return False
        return check_password(code, self.code_hash)
