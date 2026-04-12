"""
Forumulários centralizados da aplicação Coverde.
Todos os formulários estão consolidados aqui para facilitar manutenção e organização.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.users.models import Product, Producer


# ============================================
# FORMULÁRIOS DE AUTENTICAÇÃO E REGISTO
# ============================================

class LoginForm(AuthenticationForm):
    """Formulário de login customizado com estilos Bulma"""
    
    username = forms.CharField(
        max_length=254,
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'seu@email.com',
            'autocomplete': 'email',
        })
    )
    
    password = forms.CharField(
        label="Palavra-passe",
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': '********',
            'autocomplete': 'current-password',
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label="Manter sessão iniciada",
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox',
        })
    )

    def clean(self):
        identifier = (self.cleaned_data.get("username") or "").strip()
        if identifier:
            User = get_user_model()
            user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()
            if user and getattr(user, "locked_until", None) and user.locked_until > timezone.now():
                until_text = timezone.localtime(user.locked_until).strftime("%Y-%m-%d %H:%M")
                raise ValidationError(f"Conta temporariamente bloqueada até {until_text}. Tente novamente mais tarde.")
        return super().clean()


class TwoFactorVerifyForm(forms.Form):
    code = forms.CharField(
        label="Código de verificação",
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "123456",
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
            }
        ),
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "phone",
            "district",
            "county",
            "parish",
            "profile_image",
            "two_factor_enabled",
            "marketing_opt_in",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input", "inputmode": "tel", "autocomplete": "tel"}),
            "district": forms.TextInput(attrs={"class": "input"}),
            "county": forms.TextInput(attrs={"class": "input"}),
            "parish": forms.TextInput(attrs={"class": "input"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "input", "accept": "image/*"}),
        }
        labels = {
            "first_name": "Nome",
            "last_name": "Apelido",
            "phone": "Telemóvel",
            "district": "Distrito",
            "county": "Concelho",
            "parish": "Freguesia",
            "profile_image": "Imagem de perfil",
            "two_factor_enabled": "Ativar 2FA por email",
            "marketing_opt_in": "Aceito comunicações",
        }


class ProducerVerificationRequestForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ["nif", "verification_document"]
        widgets = {
            "nif": forms.TextInput(attrs={"class": "input", "placeholder": "501234567"}),
            "verification_document": forms.ClearableFileInput(attrs={"class": "input"}),
        }
        labels = {
            "nif": "NIF",
            "verification_document": "Documento de verificação",
        }


class BaseRegisterForm(forms.ModelForm):
    """Formulário base para registo com encriptação de password"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': '••••••••',
        }),
        label="Palavra-passe"
    )

    accept_privacy_policy = forms.BooleanField(
        required=True,
        label="Li e aceito a Política de Privacidade (RGPD)",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
        error_messages={"required": "Precisa aceitar a Política de Privacidade para criar a conta."},
    )

    accept_terms = forms.BooleanField(
        required=True,
        label="Li e aceito os Termos de Utilização",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
        error_messages={"required": "Precisa aceitar os Termos de Utilização para criar a conta."},
    )

    marketing_opt_in = forms.BooleanField(
        required=False,
        label="Quero receber comunicações (opcional)",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "district",
            "county",
            "parish",
            "password",
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'nome.usuario',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Primeiro nome',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Apelido',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'seu@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': '912345678 ou +351912345678',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }),
            'district': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Distrito',
            }),
            'county': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Concelho',
            }),
            'parish': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Freguesia',
            }),
        }
        labels = {
            "username": "Nome de utilizador",
            "first_name": "Nome",
            "last_name": "Apelido",
            "email": "Email",
            "phone": "Telemóvel",
            "district": "Distrito",
            "county": "Concelho",
            "parish": "Freguesia",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("first_name", "last_name", "phone", "district", "county", "parish"):
            if field_name in self.fields:
                self.fields[field_name].required = True

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not phone:
            return phone

        # Normalizar formatos comuns: espaços, hífens, parênteses
        for ch in (" ", "-", "(", ")", ".", "\u00A0"):
            phone = phone.replace(ch, "")

        # Permitir "00" como prefixo internacional
        if phone.startswith("00"):
            phone = "+" + phone[2:]

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        if self.cleaned_data.get("accept_privacy_policy"):
            user.accepted_privacy_policy_at = timezone.now()

        if self.cleaned_data.get("accept_terms"):
            user.accepted_terms_at = timezone.now()

        marketing_opt_in = bool(self.cleaned_data.get("marketing_opt_in"))
        user.marketing_opt_in = marketing_opt_in
        if marketing_opt_in and not user.marketing_opt_in_at:
            user.marketing_opt_in_at = timezone.now()
        if commit:
            user.save()
        return user


class ConsumerRegisterForm(BaseRegisterForm):
    """Formulário de registo para consumidores"""
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "consumer"
        user.is_verified = False
        if commit:
            user.save()
        return user


class ProducerRegisterForm(BaseRegisterForm):
    """Formulário de registo para produtores com campos específicos"""
    
    producer_name = forms.CharField(
        required=True,
        max_length=255,
        label="Nome da Exploração/Marca",
        help_text="Nome da sua exploração ou marca",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Ex: Quinta Bio do Norte',
        })
    )
    producer_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 4,
            'class': 'textarea',
            'placeholder': 'Descreva a sua produção...',
        }),
        label="Descrição",
        help_text="Pequena descrição sobre a sua produção ou empresa",
    )
    producer_location = forms.CharField(
        required=False,
        max_length=255,
        label="Localização",
        help_text="Cidade, região ou zona de entrega",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Ex: Porto, Norte de Portugal',
        })
    )

    nif = forms.CharField(
        required=False,
        max_length=20,
        label="NIF",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "501234567",
        }),
        help_text="Obrigatório para verificação do produtor (pode preencher agora ou depois).",
    )

    verification_document = forms.FileField(
        required=False,
        label="Documento de verificação (opcional)",
        help_text="Ex.: declaração de atividade agrícola, etc. Pode enviar agora ou depois.",
        widget=forms.ClearableFileInput(attrs={"class": "input"}),
    )

    producer_public_profile_consent = forms.BooleanField(
        required=True,
        label="Compreendo que o nome/marca e a localização poderão ser visíveis para consumidores",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
        error_messages={"required": "Precisa confirmar para criar uma conta de produtor."},
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "producer"
        user.is_verified = False
        if self.cleaned_data.get("producer_public_profile_consent"):
            user.producer_public_profile_consent_at = timezone.now()
        if commit:
            user.save()
        return user

class Meta(BaseRegisterForm.Meta):
        fields = BaseRegisterForm.Meta.fields + [
            "producer_name",
            "producer_description",
            "producer_location",
            "nif",
            "verification_document",
        ]


# ============================================
# FORMULÁRIOS DE ENCOMENDAS / CHECKOUT
# ============================================

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        label="Morada de entrega",
        widget=forms.Textarea(attrs={"class": "textarea", "rows": 3, "placeholder": "Rua, nº, localidade, código postal"}),
    )
    shipping_contact = forms.CharField(
        label="Contacto de entrega",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "912345678", "autocomplete": "tel"}),
    )


# ============================================
# FORMULÁRIOS DE PRODUTOS
# ============================================

class ProductForm(forms.ModelForm):
    """Formulário para criação e edição de produtos"""
    
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "certification",
            "price",
            "unit",
            "stock",
            "main_image",
            "is_active",
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ex: Tomate Cereja Orgânico',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Descreva o seu produto...',
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                'required': True,
            }),
            'certification': forms.Select(),
            'price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'required': True,
            }),
            'unit': forms.Select(attrs={'required': True}),
            'stock': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': '0',
                'min': '0',
                'required': True,
            }),
            'main_image': forms.ClearableFileInput(attrs={'class': 'input', 'accept': 'image/*'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        labels = {
            'name': 'Nome do Produto',
            'description': 'Descrição',
            'category': 'Categoria',
            'certification': 'Certificação',
            'price': 'Preço (€)',
            'unit': 'Unidade',
            'stock': 'Quantidade em Stock',
            'main_image': 'Imagem principal',
            'is_active': 'Ativo para venda',
        }
