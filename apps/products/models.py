import re

from django.core.exceptions import ValidationError

from apps.users.models import Producer


def validate_portuguese_nif(value):
    if not value:
        return

    nif = re.sub(r'[-\s]', '', value)
    if not nif.isdigit() or len(nif) != 9:
        raise ValidationError('O NIF deve ter 9 dígitos numéricos.')
    if nif[0] not in '1235689':
        raise ValidationError('NIF inválido. Deve começar com 1,2,3,5,6,8 ou 9.')


class ProducerProfile(Producer):
    """
    Camada de compatibilidade para código legado do app products.

    O produtor ativo do marketplace é `apps.users.models.Producer`.
    Este proxy mantém imports antigos sem reintroduzir um segundo modelo
    concreto com schema e regras próprios.
    """

    class Meta:
        proxy = True
        verbose_name = 'Perfil de Produtor'
        verbose_name_plural = 'Perfis de Produtores'
