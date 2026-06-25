from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model with extended fields for Coverde"""
    
    USER_TYPE_CHOICES = (
        ('consumer', 'Consumer'),
        ('producer', 'Producer'),
        ('admin', 'Administrator'),
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='consumer'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    
    # RGPD Consent Fields
    accepted_terms_at = models.DateTimeField(null=True, blank=True)
    accepted_privacy_policy_at = models.DateTimeField(null=True, blank=True)
    marketing_opt_in = models.BooleanField(default=False)
    marketing_opt_in_at = models.DateTimeField(null=True, blank=True)
    
    # Right to Erasure
    data_deleted_at = models.DateTimeField(null=True, blank=True)
    deletion_requested_at = models.DateTimeField(null=True, blank=True)
    
    # Security
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users_auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def is_producer(self):
        return self.user_type == 'producer'
    
    def is_consumer(self):
        return self.user_type == 'consumer'
    
    def is_admin_user(self):
        return self.user_type == 'admin' or self.is_superuser


class EmailVerificationToken(models.Model):
    """Email verification tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users_auth_emailverificationtoken'
        verbose_name = 'Email Verification Token'
        verbose_name_plural = 'Email Verification Tokens'
    
    def __str__(self):
        return f'{self.user.email} - {self.created_at}'


class TwoFactorCode(models.Model):
    """Two-factor authentication codes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='two_factor_codes')
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users_auth_twofactorcode'
        verbose_name = 'Two-Factor Code'
        verbose_name_plural = 'Two-Factor Codes'
