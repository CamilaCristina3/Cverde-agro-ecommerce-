"""
COVERDE - apps/users/forms.py
Formulários de registo, login e perfil (Portugal).
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Address  # ← Importação correta

User = get_user_model()


class ClientRegisterForm(forms.ModelForm):
    """Formulário de registo de cliente (Portugal)."""

    password = forms.CharField(
        label='Palavra-passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Confirmar palavra-passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a palavra-passe'})
    )
    terms = forms.BooleanField(
        label='Aceito os Termos e Condições do COVERDE',
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O seu nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O seu apelido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+351 912 345 678'}),  # ← Portugal
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está registado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('As palavras-passe não coincidem.')
        return cleaned_data


class ProducerRegisterForm(forms.ModelForm):
    """Formulário de registo de produtor (Portugal)."""

    password = forms.CharField(
        label='Palavra-passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Confirmar palavra-passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a palavra-passe'})
    )
    company_name = forms.CharField(
        label='Nome da empresa / cooperativa',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional para produtores individuais'})
    )
    farm_name = forms.CharField(
        label='Nome da exploração agrícola',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Quinta Verde do Vale'})
    )
    district = forms.CharField(  # ← Portugal: Distrito
        label='Distrito',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Coimbra, Lisboa, Porto...'})
    )
    county = forms.CharField(  # ← Portugal: Concelho
        label='Concelho',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Coimbra, Sintra, Vila Nova de Gaia...'})
    )
    terms = forms.BooleanField(
        label='Aceito os Termos e Condições do COVERDE',
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O seu nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O seu apelido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+351 912 345 678'}),  # ← Portugal
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está registado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As palavras-passe não coincidem.')
        return cleaned_data


class CoverdeLoginForm(AuthenticationForm):
    """Formulário de login personalizado para COVERDE."""

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'O seu email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Palavra-passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'A sua palavra-passe'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Formulário de edição de perfil (Portugal)."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+351 912 345 678'}),  # ← Portugal
        }


class AddressForm(forms.ModelForm):
    """Formulário de morada de entrega (Portugal)."""

    class Meta:
        model = Address
        fields = ['label', 'full_name', 'phone', 'street', 'city', 'district', 'postal_code', 'is_default']  # ← Portugal
        widgets = {
            'label': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+351 912 345 678'}),  # ← Portugal
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número, andar'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Distrito'}),  # ← Portugal
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3000-000'}),  # ← Portugal
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['is_default'].help_text = 'Marcar como morada padrão para entregas.'
