"""
COVERDE - apps/users/admin.py
Administração dos modelos da app users (Portugal).
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import CustomerProfile, SupplierProfile, Address, AccountActivationToken, Notification
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
        from django.utils import timezone
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