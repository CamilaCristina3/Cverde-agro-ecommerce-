from django.contrib import admin, messages
from django.utils import timezone

from apps.users.models import Producer
from .models import ProducerCertification


# Evita erro caso Producer já esteja registado noutro admin.py
if admin.site.is_registered(Producer):
    admin.site.unregister(Producer)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    """
    Administração dos produtores COVERDE.
    """

    list_display = (
        "id",
        "name",
        "user_email",
        "location",
        "status",
        "is_verified",
        "rating",
        "is_active",
        "created_at",
    )

    list_filter = (
        "status",
        "is_verified",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "nif",
        "location",
    )

    readonly_fields = (
        "rating",
        "total_ratings",
        "created_at",
        "updated_at",
        "verified_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    actions = (
        "approve_producers",
        "reject_producers",
        "activate_producers",
        "deactivate_producers",
    )

    fieldsets = (
        (
            "Informação do Produtor",
            {
                "fields": (
                    "user",
                    "name",
                    "description",
                    "location",
                    "nif",
                )
            },
        ),
        (
            "Verificação",
            {
                "fields": (
                    "status",
                    "is_verified",
                    "verified_at",
                    "verified_by",
                    "rejection_reason",
                    "verification_document",
                )
            },
        ),
        (
            "Avaliação",
            {
                "fields": (
                    "rating",
                    "total_ratings",
                )
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "is_active",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def user_email(self, obj):
        if obj.user:
            return obj.user.email
        return "-"

    user_email.short_description = "Email"

    def approve_producers(self, request, queryset):
        updated = queryset.update(
            status="approved",
            is_verified=True,
            verified_at=timezone.now(),
            verified_by=request.user,
            is_active=True,
            rejection_reason="",
        )

        self.message_user(
            request,
            f"{updated} produtor(es) aprovado(s) com sucesso.",
            messages.SUCCESS,
        )

    approve_producers.short_description = "Aprovar produtores selecionados"

    def reject_producers(self, request, queryset):
        updated = queryset.update(
            status="rejected",
            is_verified=False,
            is_active=False,
        )

        self.message_user(
            request,
            f"{updated} produtor(es) rejeitado(s).",
            messages.WARNING,
        )

    reject_producers.short_description = "Rejeitar produtores selecionados"

    def activate_producers(self, request, queryset):
        updated = queryset.update(is_active=True)

        self.message_user(
            request,
            f"{updated} produtor(es) ativado(s).",
            messages.SUCCESS,
        )

    activate_producers.short_description = "Ativar produtores selecionados"

    def deactivate_producers(self, request, queryset):
        updated = queryset.update(is_active=False)

        self.message_user(
            request,
            f"{updated} produtor(es) desativado(s).",
            messages.WARNING,
        )

    deactivate_producers.short_description = "Desativar produtores selecionados"


@admin.register(ProducerCertification)
class ProducerCertificationAdmin(admin.ModelAdmin):
    """
    Administração das certificações dos produtores.
    """

    list_display = (
        "id",
        "producer",
        "cert_type",
        "certificate_number",
        "issue_date",
        "expiry_date",
        "is_valid",
        "created_at",
    )

    list_filter = (
        "cert_type",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "producer__name",
        "producer__user__email",
        "certificate_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    fieldsets = (
        (
            "Produtor",
            {
                "fields": (
                    "producer",
                )
            },
        ),
        (
            "Dados da Certificação",
            {
                "fields": (
                    "cert_type",
                    "certificate_number",
                    "issue_date",
                    "expiry_date",
                    "document",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def is_valid(self, obj):
        if obj.expiry_date and obj.expiry_date < timezone.now().date():
            return "Expirada"
        return "Válida"

    is_valid.short_description = "Validade"