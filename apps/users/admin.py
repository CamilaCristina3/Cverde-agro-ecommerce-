"""
COVERDE - apps/users/admin.py
Administração dos modelos da app users (Portugal).
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import (
    CustomerProfile,
    SupplierProfile,
    Address,
    AccountActivationToken,
    Notification,
    Producer,
    Product,
    Category,
)
# Nota: User é gerido em apps.users_auth.admin.py (AUTH_USER_MODEL)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Administração de perfis de clientes (Portugal)."""

    list_display = ['user', 'gender', 'newsletter_subscribed', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    list_filter = ['gender', 'newsletter_subscribed']


@admin.register(SupplierProfile)
class SupplierProfileAdmin(admin.ModelAdmin):
    """Administração de perfis de produtores (Portugal)."""

    list_display = ['company_name', 'user', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['company_name', 'user__email', 'nif']  # ← NIF (Portugal)
    actions = ['approve_suppliers', 'reject_suppliers']

    def approve_suppliers(self, request, queryset):
        """Aprovar produtores selecionados."""
        queryset.update(
            status=SupplierProfile.Status.APPROVED,
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, 'Produtores aprovados com sucesso.')  # ← Portugal
    approve_suppliers.short_description = 'Aprovar produtores selecionados'  # ← Portugal

    def reject_suppliers(self, request, queryset):
        """Rejeitar produtores selecionados."""
        queryset.update(status=SupplierProfile.Status.REJECTED)
        self.message_user(request, 'Produtores rejeitados.')  # ← Portugal
    reject_suppliers.short_description = 'Rejeitar produtores selecionados'  # ← Portugal


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Administração de moradas (Portugal)."""

    list_display = ['user', 'label', 'city', 'district', 'is_default']  # ← Portugal: district
    list_filter = ['label', 'is_default']
    search_fields = ['user__email', 'city', 'district', 'street']  # ← Portugal: district


@admin.register(AccountActivationToken)
class AccountActivationTokenAdmin(admin.ModelAdmin):
    """Administração de tokens de ativação."""

    list_display = ['user', 'token', 'is_used', 'is_valid_display', 'expires_at', 'created_at']
    list_filter = ['is_used']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at']

    def is_valid_display(self, obj):
        if obj.is_valid:
            return format_html('<span style="color:green">✓ Válido</span>')
        return format_html('<span style="color:red">✗ Expirado/Usado</span>')
    is_valid_display.short_description = 'Estado'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Administração de notificações."""

    list_display = ['user', 'title', 'notif_type', 'is_read', 'created_at']
    list_filter = ['notif_type', 'is_read']
    search_fields = ['user__email', 'title']


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    """Administração de produtores com ações de aprovação."""

    list_display = ['name', 'user', 'status', 'is_verified', 'is_active', 'rating', 'created_at']
    list_filter = ['status', 'is_verified', 'is_active', 'created_at']
    search_fields = ['name', 'user__email', 'nif', 'location']
    actions = ['approve_producers', 'suspend_producers', 'reject_producers']

    def approve_producers(self, request, queryset):
        now = timezone.now()
        queryset.update(
            status=Producer.Status.APPROVED,
            is_verified=True,
            verified_at=now,
            verified_by=request.user,
            is_active=True,
        )
        self.message_user(request, 'Produtores aprovados com sucesso.')
    approve_producers.short_description = 'Aprovar produtores selecionados'

    def suspend_producers(self, request, queryset):
        queryset.update(status=Producer.Status.SUSPENDED, is_active=False)
        self.message_user(request, 'Produtores suspensos com sucesso.')
    suspend_producers.short_description = 'Suspender produtores selecionados'

    def reject_producers(self, request, queryset):
        queryset.update(status=Producer.Status.REJECTED, is_active=False)
        self.message_user(request, 'Produtores rejeitados.')
    reject_producers.short_description = 'Rejeitar produtores selecionados'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'ordering']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'producer', 'category', 'price', 'stock', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'is_featured', 'category']
    search_fields = ['name', 'slug', 'producer__name']
    actions = ['activate_products', 'deactivate_products']

    def activate_products(self, request, queryset):
        queryset.update(status='active', is_active=True)
        self.message_user(request, 'Produtos ativados com sucesso.')
    activate_products.short_description = 'Ativar produtos selecionados'

    def deactivate_products(self, request, queryset):
        queryset.update(status='inactive', is_active=False)
        self.message_user(request, 'Produtos desativados com sucesso.')
    deactivate_products.short_description = 'Desativar produtos selecionados'
