from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'producer', 'status', 'rating', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'producer__name')
    prepopulated_fields = {'slug': ('name',)}
    actions = ('activate_stores', 'suspend_stores')

    @admin.action(description='Ativar lojas selecionadas')
    def activate_stores(self, request, queryset):
        updated = queryset.update(status=Store.Status.ACTIVE, is_active=True)
        self.message_user(request, f'{updated} loja(s) ativada(s).')

    @admin.action(description='Suspender lojas selecionadas')
    def suspend_stores(self, request, queryset):
        updated = queryset.update(status=Store.Status.SUSPENDED, is_active=False)
        self.message_user(request, f'{updated} loja(s) suspensa(s).')
