"""
Configuração do Django Admin para o Coverde
Organização profissional dos modelos para facilitar a gestão
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import (
    User,
    Producer,
    Category,
    Product,
    Order,
    OrderItem,
    Payment,
    Notification,
    NotificationPreference,
    Review,
    Cart,
    ConsentLog,
    EmailVerificationToken,
    TwoFactorCode,
)


# ============================================
# 1. ADMIN DO UTILIZADOR (USER)
# ============================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuração personalizada do Admin para o modelo User
    Organização por secções para facilitar a gestão
    """

    list_display = (
        "id",
        "username",
        "email",
        "get_full_name",
        "user_type",
        "is_verified",
        "two_factor_enabled",
        "is_active",
        "date_joined",
        "display_avatar",
    )

    list_filter = (
        "user_type",
        "is_verified",
        "two_factor_enabled",
        "is_active",
        "is_superuser",
        "date_joined",
        "marketing_opt_in",
    )

    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("-date_joined",)
    list_editable = ("user_type", "is_verified", "two_factor_enabled", "is_active")
    list_per_page = 25
    date_hierarchy = "date_joined"

    actions = ["mark_as_verified", "mark_as_unverified", "export_users_data"]

    fieldsets = (
        (_("Informação Pessoal"), {
            "fields": (
                ("username", "email"),
                ("first_name", "last_name"),
                "phone",
                ("user_type", "profile_image"),
            )
        }),
        (_("Localização (Portugal)"), {
            "fields": (("district", "county", "parish"),),
            "classes": ("collapse",),
        }),
        (_("Permissões e Acessos"), {
            "fields": (
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            "classes": ("collapse",),
        }),
        (_("Segurança e Autenticação"), {
            "fields": (
                "password",
                ("login_attempts", "locked_until"),
                "last_login_ip",
                "last_login",
            ),
            "classes": ("collapse",),
        }),
        (_("Consentimentos RGPD"), {
            "fields": (
                ("accepted_terms_at", "accepted_privacy_policy_at"),
                ("marketing_opt_in", "marketing_opt_in_at"),
                "producer_public_profile_consent_at",
            ),
            "classes": ("collapse",),
        }),
        (_("Direito ao Esquecimento (RGPD)"), {
            "fields": (
                ("data_exported_at", "data_deleted_at"),
                "deletion_requested_at",
            ),
            "classes": ("collapse",),
        }),
        (_("Datas Importantes"), {
            "fields": ("date_joined",),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "user_type"),
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name() or "-"

    get_full_name.short_description = "Nome completo"
    get_full_name.admin_order_field = "first_name"

    def display_avatar(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_image.url,
            )
        icons = {
            "consumer": "👤",
            "producer": "🌱",
            "admin": "👑",
        }
        return format_html('<span style="font-size: 24px;">{}</span>', icons.get(obj.user_type, "👤"))

    display_avatar.short_description = "Avatar"

    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} utilizador(es) marcado(s) como verificado(s).")

    mark_as_verified.short_description = "Marcar como verificado"

    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} utilizador(es) marcado(s) como não verificado(s).")

    mark_as_unverified.short_description = "Marcar como não verificado"

    def export_users_data(self, request, queryset):
        import csv

        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="coverde_utilizadores.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Username", "Email", "Nome", "Tipo", "Verificado", "Data Registo"])

        for user in queryset:
            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.get_full_name(),
                user.get_user_type_display(),
                "Sim" if user.is_verified else "Não",
                user.date_joined.strftime("%Y-%m-%d %H:%M"),
            ])

        return response

    export_users_data.short_description = "Exportar dados selecionados (CSV)"


# ============================================
# 2. ADMIN DO PRODUTOR (PRODUCER)
# ============================================

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user_email", "is_verified", "rating", "total_products", "created_at")
    list_filter = ("is_verified", "is_active", "created_at")
    search_fields = ("name", "user__email", "user__first_name", "user__last_name", "nif")
    list_editable = ("is_verified",)
    list_per_page = 25
    date_hierarchy = "created_at"

    fieldsets = (
        (_("Informação do Produtor"), {
            "fields": ("user", "name", "description", "location"),
        }),
        (_("Documentação e Verificação"), {
            "fields": ("nif", "verification_document", "is_verified", "verified_at", "verified_by"),
            "classes": ("collapse",),
        }),
        (_("Métricas"), {
            "fields": ("rating", "total_ratings", "total_products", "total_sales"),
            "classes": ("collapse",),
        }),
        (_("Status"), {"fields": ("is_active",)}),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"
    user_email.admin_order_field = "user__email"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(user_type="producer").order_by("email", "username")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ============================================
# 3. ADMIN DE CATEGORIAS (CATEGORY)
# ============================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "parent", "is_active", "order")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    list_editable = ("is_active", "order")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25


# ============================================
# 4. ADMIN DE PRODUTOS (PRODUCT)
# ============================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "producer_name",
        "category",
        "price",
        "stock",
        "average_rating",
        "is_active",
        "is_featured",
    )
    list_filter = ("category", "certification", "is_active", "is_featured", "created_at")
    search_fields = ("name", "producer__name", "producer__user__email")
    list_editable = ("price", "stock", "is_active", "is_featured")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("average_rating", "total_reviews", "total_sold")

    fieldsets = (
        (_("Informação Básica"), {
            "fields": ("producer", "name", "slug", "description", "category", "certification"),
        }),
        (_("Preço e Stock"), {"fields": ("price", "stock", "unit")}),
        (_("Imagens"), {"fields": ("main_image", "extra_images")}),
        (_("Métricas"), {
            "fields": ("average_rating", "total_reviews", "total_sold"),
            "classes": ("collapse",),
        }),
        (_("Status"), {"fields": ("is_active", "is_featured")}),
    )

    def producer_name(self, obj):
        return obj.producer.name

    producer_name.short_description = "Produtor"
    producer_name.admin_order_field = "producer__name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("producer", "category")


# ============================================
# 5. ADMIN DE ENCOMENDAS (ORDER)
# ============================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "total", "status", "created_at", "paid_at", "has_invoice")
    list_filter = ("status", "created_at", "paid_at")
    search_fields = ("id", "user__email", "user__first_name", "user__last_name", "invoice_number")
    list_editable = ("status",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("subtotal", "shipping_cost", "vat", "total", "invoice_number", "created_at")
    inlines = [OrderItemInline]

    fieldsets = (
        (_("Cliente"), {"fields": ("user", "shipping_address", "shipping_contact")}),
        (_("Valores"), {"fields": ("subtotal", "shipping_cost", "vat", "total")}),
        (_("Status e Pagamento"), {"fields": ("status", "tracking_code", "paid_at", "delivered_at")}),
        (_("Faturação"), {"fields": ("invoice_number", "invoice_pdf"), "classes": ("collapse",)}),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Cliente"
    user_email.admin_order_field = "user__email"

    def has_invoice(self, obj):
        return bool(obj.invoice_pdf)

    has_invoice.boolean = True
    has_invoice.short_description = "Fatura"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


# ============================================
# 6. ADMIN DE PAGAMENTOS (PAYMENT)
# ============================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "method", "amount", "status", "paid_at")
    list_filter = ("method", "status", "created_at")
    search_fields = ("order__id", "transaction_id", "reference")
    list_editable = ("status",)
    list_per_page = 25
    readonly_fields = ("transaction_id", "reference", "webhook_data")

    fieldsets = (
        (_("Dados do Pagamento"), {"fields": ("order", "method", "amount", "status")}),
        (_("Referências"), {"fields": ("transaction_id", "reference", "entity"), "classes": ("collapse",)}),
        (_("Dados do Cartão (anonimizados)"), {"fields": ("card_last4", "card_brand"), "classes": ("collapse",)}),
        (_("Webhook"), {"fields": ("webhook_received_at", "webhook_data"), "classes": ("collapse",)}),
    )


# ============================================
# 7. ADMIN DE NOTIFICAÇÕES (NOTIFICATION)
# ============================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user_email", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("title", "message", "user__email")
    list_per_page = 25
    date_hierarchy = "created_at"

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Utilizador"
    user_email.admin_order_field = "user__email"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "email_enabled", "push_enabled", "order_updates", "marketing_emails")
    list_filter = ("email_enabled", "push_enabled", "order_updates", "marketing_emails")
    search_fields = ("user__email",)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Utilizador"
    user_email.admin_order_field = "user__email"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


# ============================================
# 8. ADMIN DE AVALIAÇÕES (REVIEW)
# ============================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    class ReviewForm(forms.ModelForm):
        """Formulário personalizado para Avaliação com validação condicional."""

        class Meta:
            model = Review
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Melhor UX no campo rating
            if "rating" in self.fields:
                self.fields["rating"].widget.attrs.update({"min": 1, "max": 5})

        def clean(self):
            cleaned_data = super().clean()
            review_type = cleaned_data.get("review_type")
            product = cleaned_data.get("product")
            producer = cleaned_data.get("producer")

            if review_type == "product":
                if not product:
                    self.add_error("product", "Este campo é obrigatório para avaliação de produto.")
                if producer:
                    self.add_error("producer", "Não deve selecionar um produtor para avaliação de produto.")

            elif review_type == "producer":
                if not producer:
                    self.add_error("producer", "Este campo é obrigatório para avaliação de produtor.")
                if product:
                    self.add_error("product", "Não deve selecionar um produto para avaliação de produtor.")

            return cleaned_data

    form = ReviewForm

    list_display = (
        "id",
        "user_email",
        "review_type",
        "review_target",
        "rating",
        "is_approved",
        "is_reported",
        "created_at",
    )
    list_filter = ("review_type", "rating", "is_approved", "is_reported", "created_at")
    search_fields = ("user__email", "comment", "product__name", "producer__name")
    list_editable = ("is_approved",)
    list_per_page = 25
    date_hierarchy = "created_at"

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (_("Informação da Avaliação"), {"fields": ("user", "review_type")}),
        (
            _("Conteúdo da Avaliação"),
            {
                "fields": ("product", "producer", "rating", "comment", "order"),
                "description": (
                    "Selecione o tipo de avaliação primeiro. "
                    "Apenas um campo (Produto ou Produtor) deve ser preenchido."
                ),
            },
        ),
        (_("Moderação"), {"fields": ("is_approved", "is_reported", "report_reason"), "classes": ("collapse",)}),
        (_("Datas"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    class Media:
        js = ("admin/js/review_dynamic.js",)
        css = {"all": ("admin/css/review_admin.css",)}

    actions = ["approve_reviews", "reject_reviews", "mark_as_reported"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Consumidor"
    user_email.admin_order_field = "user__email"

    def review_target(self, obj):
        if obj.product:
            return format_html('<span class="tag tag-product">Produto</span> {}', obj.product.name)
        if obj.producer:
            return format_html('<span class="tag tag-producer">Produtor</span> {}', obj.producer.name)
        return "-"

    review_target.short_description = "Alvo"

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True, is_reported=False)
        self.message_user(request, f"{updated} avaliação(ões) aprovada(s).")

    approve_reviews.short_description = "Aprovar avaliações selecionadas"

    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} avaliação(ões) rejeitada(s).")

    reject_reviews.short_description = "Rejeitar avaliações selecionadas"

    def mark_as_reported(self, request, queryset):
        updated = queryset.update(is_reported=True)
        self.message_user(request, f"{updated} avaliação(ões) marcada(s) como denunciada(s).")

    mark_as_reported.short_description = "Marcar como denunciada"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "product", "producer")


# ============================================
# 9. ADMIN DE CONSENTIMENTOS RGPD (CONSENTLOG)
# ============================================

@admin.register(ConsentLog)
class ConsentLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "consent_type", "status", "ip_address", "created_at")
    list_filter = ("consent_type", "status", "created_at")
    search_fields = ("user__email", "ip_address")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("consent_type", "status", "ip_address", "user_agent", "document_version")

    def user_email(self, obj):
        return obj.user.email if obj.user else "Anónimo"

    user_email.short_description = "Utilizador"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# ============================================
# 10. ADMIN DE CARRINHO (CART)
# ============================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "session_key", "items_count", "created_at", "updated_at")
    search_fields = ("session_key",)
    list_per_page = 25
    readonly_fields = ("session_key", "items")

    def items_count(self, obj):
        return len(obj.items or [])

    items_count.short_description = "Total de itens"

    def has_add_permission(self, request):
        return False


# ============================================
# 11. SEGURANÇA / TOKENS (RF02 / RF04)
# ============================================

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token", "created_at", "used_at")
    list_filter = ("used_at",)
    search_fields = ("user__email", "token")


@admin.register(TwoFactorCode)
class TwoFactorCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "expires_at", "used_at")
    list_filter = ("used_at",)
    search_fields = ("user__email",)


admin.site.site_header = "Coverde - Administração"
admin.site.site_title = "Painel Coverde"
admin.site.index_title = "Bem-vindo ao painel de administração do Coverde"
