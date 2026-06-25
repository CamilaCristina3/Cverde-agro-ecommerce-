from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Basic', {'fields': ('name', 'slug', 'description', 'parent')}),
        ('Display', {'fields': ('icon', 'image', 'order')}),
        ('Status', {'fields': ('is_active',)}),
    )
