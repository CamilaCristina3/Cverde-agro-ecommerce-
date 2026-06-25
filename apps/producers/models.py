from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.users_auth.models import User


class Producer(models.Model):
    """Agricultural producer/farmer profile"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producer')
    name = models.CharField(max_length=200)  # Farm/business name
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    nif = models.CharField(max_length=20, blank=True)  # Tax ID
    verification_document = models.FileField(upload_to='producers/verification/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_producers')
    rejection_reason = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'producers_producer'
        verbose_name = 'Producer'
        verbose_name_plural = 'Producers'
    
    def __str__(self):
        return self.name


class ProducerCertification(models.Model):
    """Certifications held by producer (Bio, DOP, etc)"""
    
    CERTIFICATION_TYPES = (
        ('organic', 'Organic (Bio)'),
        ('dop', 'DOP - Protected Designation'),
        ('pig', 'PGI - Protected Geographical Indication'),
        ('fair_trade', 'Fair Trade'),
        ('other', 'Other'),
    )
    
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='certifications')
    cert_type = models.CharField(max_length=50, choices=CERTIFICATION_TYPES)
    name = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_number = models.CharField(max_length=100, blank=True)
    document = models.FileField(upload_to='producers/certifications/')
    
    class Meta:
        db_table = 'producers_producercertification'
        verbose_name = 'Producer Certification'
        verbose_name_plural = 'Producer Certifications'
    
    def __str__(self):
        return f'{self.producer.name} - {self.get_cert_type_display()}'
