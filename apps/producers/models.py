"""
COVERDE - apps/producers/models.py
Modelos de produtor.
NOTA: O modelo Producer principal está em apps/users/models.py.
Aqui estão apenas modelos auxiliares.
"""

from django.db import models
from django.utils import timezone

from apps.users.models import Producer


class ProducerCertification(models.Model):
    """
    Certificações do produtor.
    Relacionado com Producer, que está em apps/users/models.py.
    """

    CERTIFICATION_TYPES = (
        ('organic', 'Biológico'),
        ('dop', 'DOP - Denominação de Origem Protegida'),
        ('igp', 'IGP - Indicação Geográfica Protegida'),
        ('integrated', 'Produção Integrada'),
        ('fair_trade', 'Comércio Justo'),
        ('other', 'Outro'),
    )

    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name='certifications',
        verbose_name='Produtor'
    )

    cert_type = models.CharField(
        max_length=50,
        choices=CERTIFICATION_TYPES,
        verbose_name='Tipo de certificação'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Nome da certificação'
    )

    issue_date = models.DateField(
        verbose_name='Data de emissão'
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de validade'
    )

    certificate_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número do certificado'
    )

    document = models.FileField(
        upload_to='producers/certifications/',
        verbose_name='Documento do certificado'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        db_table = 'producers_producercertification'
        verbose_name = 'Certificação do Produtor'
        verbose_name_plural = 'Certificações do Produtor'
        ordering = ['-issue_date']

    def __str__(self):
        return f'{self.producer.name} - {self.get_cert_type_display()}'