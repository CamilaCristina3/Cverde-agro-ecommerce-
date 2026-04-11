from django.contrib import admin

from .models import Producer


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "location", "rating", "active")
    list_filter = ("active",)
    search_fields = ("name", "user__username", "location")
