"""
Formulários centralizados da aplicação Coverde.
Todos os formulários estão consolidados aqui para facilitar manutenção.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

# ✅ Importações corrigidas
from apps.users.models import Product, Producer  # ← Producer em users
from apps.reviews.models import Review

# Buscar o modelo User
User = get_user_model()


# ============================================
# FORMULÁRIOS DE AUTENTICAÇÃO E REGISTO
# ============================================

class LoginForm(AuthenticationForm):
    """Formulário de login"""
    
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
        })
    )
    
    password = forms.CharField(
        label="Palavra-passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label="Lembrar-me",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        email = self.cleaned_data.get("username", "").strip()
        if email:
            user = User.objects.filter(email__iexact=email).first()
            if user and user.locked_until and user.locked_until > timezone.now():
                raise ValidationError(f"Conta bloqueada até {user.locked_until.strftime('%d/%m/%Y %H:%M')}")
        return super().clean()


class TwoFactorVerifyForm(forms.Form):
    """Formulário de verificação 2FA"""
    code = forms.CharField(
        label="Código de verificação",
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123456",
            "inputmode": "numeric",
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Formulário de atualização de perfil"""
    
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "phone",
            "profile_image", "two_factor_enabled", "marketing_opt_in"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "district": forms.TextInput(attrs={"class": "form-control"}),
            "county": forms.TextInput(attrs={"class": "form-control"}),
            "parish": forms.TextInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "first_name": "Nome",
            "last_name": "Apelido",
            "phone": "Telemóvel",
            "district": "Distrito",
            "county": "Concelho",
            "parish": "Freguesia",
            "profile_image": "Foto de perfil",
            "two_factor_enabled": "Ativar verificação em dois passos (2FA)",
            "marketing_opt_in": "Receber ofertas por email",
        }


class ProducerVerificationRequestForm(forms.ModelForm):
    """Formulário para produtor pedir verificação"""
    
    class Meta:
        model = Producer  # ← Agora importado de users
        fields = ["nif", "verification_document"]
        widgets = {
            "nif": forms.TextInput(attrs={"class": "form-control", "placeholder": "501234567"}),
            "verification_document": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "nif": "NIF",
            "verification_document": "Documento de verificação",
        }


class BaseRegisterForm(forms.ModelForm):
    """Formulário base de registo (comum para consumidor e produtor)"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'autocomplete': 'new-password',
        }),
        label="Palavra-passe"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'autocomplete': 'new-password',
        }),
        label="Confirmar palavra-passe"
    )
    
    # Consentimentos obrigatórios
    accept_privacy_policy = forms.BooleanField(
        required=True,
        label="Aceito a Política de Privacidade",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={"required": "Precisa aceitar a Política de Privacidade."}
    )
    
    accept_terms = forms.BooleanField(
        required=True,
        label="Aceito os Termos de Utilização",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={"required": "Precisa aceitar os Termos de Utilização."}
    )
    
    marketing_opt_in = forms.BooleanField(
        required=False,
        label="Receber novidades por email",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email",
            "phone", "password"
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nome.usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apelido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '912345678'}),
        }
        labels = {
            "username": "Utilizador",
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
        # O username técnico é sempre o email; não expor campo manual.
        if "username" in self.fields:
            self.fields["username"].required = False
            self.fields["username"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        email = (cleaned_data.get("email") or "").strip().lower()
        if not email:
            self.add_error("email", "O email é obrigatório.")
        else:
            existing = User.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                self.add_error("email", "Já existe uma conta registada com este email.")

        cleaned_data["email"] = email
        cleaned_data["username"] = email

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError({"password2": "As palavras-passe não coincidem."})
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = (self.cleaned_data.get("email") or "").strip().lower()
        user.username = user.email
        user.set_password(self.cleaned_data["password"])
        
        # Registar consentimentos
        if self.cleaned_data.get("accept_privacy_policy"):
            user.accepted_privacy_policy_at = timezone.now()
        if self.cleaned_data.get("accept_terms"):
            user.accepted_terms_at = timezone.now()
        
        user.marketing_opt_in = self.cleaned_data.get("marketing_opt_in", False)
        if user.marketing_opt_in and not user.marketing_opt_in_at:
            user.marketing_opt_in_at = timezone.now()
        
        if commit:
            user.save()
        return user


class RegistrationForm(BaseRegisterForm):
    ACCOUNT_TYPE_CHOICES = [
        ("consumer", "Consumidor"),
        ("producer", "Produtor"),
    ]

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        initial="consumer",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Tipo de conta"
    )

    producer_name = forms.CharField(
        required=False,
        max_length=255,
        label="Nome da exploração",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Quinta do Sol'})
    )
    producer_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, 'class': 'form-control', 'placeholder': 'Descreva a sua produção...'}),
        label="Descrição"
    )
    producer_location = forms.CharField(
        required=False,
        max_length=255,
        label="Localização",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sintra'})
    )
    nif = forms.CharField(
        required=False,
        max_length=20,
        label="NIF",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "501234567"})
    )
    verification_document = forms.FileField(
        required=False,
        label="Documento de verificação",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    producer_public_profile_consent = forms.BooleanField(
        required=False,
        label="Autorizo que o nome da minha exploração seja visível para os consumidores",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(BaseRegisterForm.Meta):
        fields = BaseRegisterForm.Meta.fields + [
            "account_type", "producer_name", "producer_description", "producer_location",
            "nif", "verification_document", "producer_public_profile_consent"
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("account_type") == "producer":
            if not cleaned_data.get("producer_name"):
                self.add_error("producer_name", "Este campo é obrigatório para produtores.")
            if not cleaned_data.get("producer_public_profile_consent"):
                self.add_error("producer_public_profile_consent", "Precisa autorizar o perfil público para continuar.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get("account_type", "consumer")
        user.is_verified = user.user_type == "consumer"
        if user.is_verified:
            user.email_verified_at = timezone.now()
        if commit:
            user.save()
            if user.user_type == "producer":
                Producer.objects.create(
                    user=user,
                    name=self.cleaned_data.get("producer_name", ""),
                    description=self.cleaned_data.get("producer_description", ""),
                    location=self.cleaned_data.get("producer_location", ""),
                    nif=self.cleaned_data.get("nif", ""),
                    verification_document=self.cleaned_data.get("verification_document"),
                )
        return user


class ConsumerRegisterForm(BaseRegisterForm):
    """Registo para consumidor"""
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "consumer"
        user.is_verified = True
        user.email_verified_at = timezone.now()
        if commit:
            user.save()
        return user


class ProducerRegisterForm(BaseRegisterForm):
    """Registo para produtor com campos extra"""
    
    producer_name = forms.CharField(
        required=True,
        max_length=255,
        label="Nome da exploração",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Quinta do Sol'})
    )
    
    producer_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, 'class': 'form-control', 'placeholder': 'Descreva a sua produção...'}),
        label="Descrição"
    )
    
    producer_location = forms.CharField(
        required=False,
        max_length=255,
        label="Localização",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sintra'})
    )
    
    nif = forms.CharField(
        required=False,
        max_length=20,
        label="NIF",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "501234567"})
    )
    
    verification_document = forms.FileField(
        required=False,
        label="Documento de verificação",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    
    producer_public_profile_consent = forms.BooleanField(
        required=True,
        label="Autorizo que o nome da minha exploração seja visível para os consumidores",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={"required": "Precisa autorizar para criar conta de produtor."}
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


# ============================================
# FORMULÁRIOS DE ENCOMENDAS
# ============================================

class CheckoutForm(forms.Form):
    """Formulário de finalização de compra"""
    
    shipping_address = forms.CharField(
        label="Morada de entrega",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Rua, número, código postal"})
    )
    
    shipping_contact = forms.CharField(
        label="Contacto para entrega",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "912345678"})
    )


# ============================================
# FORMULÁRIOS DE AVALIAÇÕES (REVIEWS)
# ============================================

class ReviewForm(forms.ModelForm):
    """Formulário para criar/editar avaliações de produtos e produtores"""
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Partilhe a sua opinião detalhada (máx 1000 caracteres)',
                'rows': 5,
                'maxlength': '1000',
            }),
        }
        labels = {
            'rating': 'Classificação',
            'comment': 'Comentário',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Não permitir editar produto/produtor no form
        self.fields.pop('product', None)
        self.fields.pop('producer', None)


# ============================================
# FORMULÁRIOS DE PRODUTOS
# ============================================

class ProductForm(forms.ModelForm):
    """Formulário para criar/editar produtos"""
    
    class Meta:
        model = Product
        fields = [
            "name", "description", "category", "certification",
            "price", "stock", "unit", "main_image", "is_active", "is_featured"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tomate Cereja'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o seu produto...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'certification': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '5.99'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nome do produto',
            'description': 'Descrição',
            'category': 'Categoria',
            'certification': 'Certificação',
            'price': 'Preço (€)',
            'stock': 'Stock',
            'unit': 'Unidade',
            'main_image': 'Imagem principal',
            'is_active': 'Ativo para venda',
            'is_featured': 'Destacar produto',
        }
