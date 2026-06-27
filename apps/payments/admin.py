from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "amount",
        "status",
        "method",
        "is_test_payment",
        "reference",
        "created_at",
    )
    list_filter = (
        "status",
        "method",
        "is_test_payment",
        "created_at",
    )
    search_fields = (
        "order__id",
        "order__customer__email",
        "reference",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = (
        "id",
        "order",
        "created_at",
        "paid_at",
        "test_approved_at",
        "reference",
    )
    fieldsets = (
        (_("Encomenda"), {
            "fields": (
                ("order", "amount"),
            )
        }),
        (_("Pagamento"), {
            "fields": (
                ("status", "method"),
                ("created_at", "paid_at"),
                "reference",
            )
        }),
        (_("Modo Teste"), {
            "fields": (
                ("is_test_payment", "test_approved_at"),
                ("test_password_used", "test_signature_used"),
            ),
            "classes": ("collapse",)
        }),
        (_("Falhas e Notas"), {
            "fields": (
                "failure_reason",
                "notes",
            ),
            "classes": ("collapse",)
        }),
    )
    
    actions = (
        "mark_as_paid",
        "mark_as_failed",
    )
    
    def is_test_badge(self, obj):
        if obj.is_test_payment:
            return "TESTE"
        return "REAL"
    is_test_badge.short_description = "Tipo"
    
    @admin.action(description="Marcar como pago")
    def mark_as_paid(self, request, queryset):
        for payment in queryset:
            payment.status = Payment.Status.PAID
            payment.paid_at = timezone.now() if not payment.paid_at else payment.paid_at
            payment.save(update_fields=["status", "paid_at", "updated_at"])
        self.message_user(request, f"{queryset.count()} pagamento(s) marcado(s) como pago.")
    
    @admin.action(description="Marcar como falha")
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status=Payment.Status.FAILED)
        self.message_user(request, f"{updated} pagamento(s) marcado(s) como falha.")
