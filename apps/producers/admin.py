from django.contrib import admin
from .models import Producer, ProducerCertification


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'rating', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('name', 'user__email', 'nif')
    readonly_fields = ('rating', 'total_ratings', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'name', 'description', 'location', 'nif')}),
        ('Verification', {'fields': ('status', 'is_verified', 'verified_at', 'verified_by', 'rejection_reason', 'verification_document')}),
        ('Rating', {'fields': ('rating', 'total_ratings')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ProducerCertification)
class ProducerCertificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'producer', 'cert_type', 'issue_date', 'expiry_date')
    list_filter = ('cert_type', 'issue_date')
    search_fields = ('producer__name', 'certificate_number')
