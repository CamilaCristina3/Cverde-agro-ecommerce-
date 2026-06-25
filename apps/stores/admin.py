from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'producer', 'status', 'rating', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'producer__name')
    prepopulated_fields = {'slug': ('name',)}
