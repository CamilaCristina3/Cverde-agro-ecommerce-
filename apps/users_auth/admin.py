from django.contrib import admin
from .models import User, EmailVerificationToken, TwoFactorCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'used_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('token', 'created_at')


@admin.register(TwoFactorCode)
class TwoFactorCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'used_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('code_hash', 'created_at')
