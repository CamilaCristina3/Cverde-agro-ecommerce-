"""
Django settings for CVerde - Agro Ecommerce project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# ========== BASE DIRECTORY ==========
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis do `.env` (se existir)
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

def config(key, default=None, cast=None):
    value = os.environ.get(key, default)
    if value is None:
        return None
    if cast is None:
        return value
    return cast(value)

# ========== SEGURANÇA ==========
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default=config("DJANGO_SECRET_KEY", default="django-insecure-change-me-in-production"),
)

# SECURITY WARNING: don't run with debug turned on in production!
def _parse_debug(value):
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in {"release", "prod", "production"}:
        return False
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid truth value: {value}")

DEBUG = config("DEBUG", default=config("DJANGO_DEBUG", default=True), cast=_parse_debug)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=config("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1"),
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)
if "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

# ========== APPLICATION DEFINITION ==========
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Local apps (Coverde)
    'apps.users',
    'apps.producers',
    'apps.products',
    'apps.orders',
    'apps.payments',
    'apps.notifications',
    'apps.pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========== DEV/TEST FLAGS ==========
# Para testes locais rápidos (não usar em produção).
DISABLE_CSRF = config("DISABLE_CSRF", default=False, cast=_parse_debug)
if DISABLE_CSRF:
    MIDDLEWARE = [m for m in MIDDLEWARE if m != "django.middleware.csrf.CsrfViewMiddleware"]

ROOT_URLCONF = 'cverde.urls'

# ========== TEMPLATES ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'apps.orders.context_processors.nav_cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'cverde.wsgi.application'

# ========== DATABASE (PostgreSQL) ==========
# SRS (2025/2026) define PostgreSQL como requisito (PostGIS-ready).
# Para desenvolvimento rápido sem Postgres, pode usar DB_USE_SQLITE=true.
DB_USE_SQLITE = config("DB_USE_SQLITE", default=False, cast=_parse_debug)
if DB_USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
            "NAME": config("DB_NAME", default="cverde"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default="postgres"),
            # Fora do Docker, "localhost" é o mais comum; no Docker Compose use DB_HOST=db.
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }

# ========== PASSWORD VALIDATION ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========== INTERNATIONALIZATION ==========
LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True
# USE_L10N removido (deprecated no Django 4+)

# ========== STATIC FILES (CSS, JavaScript, Images) ==========
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ========== MEDIA FILES (uploads) ==========
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========== DEFAULT PRIMARY KEY FIELD TYPE ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== CUSTOM USER MODEL ==========
AUTH_USER_MODEL = 'users.User'

# ========== AUTHENTICATION BACKENDS ==========
AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ========== LOGIN/LOGOUT URLs ==========
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'home'

# ========== EMAIL CONFIGURATION (development) ==========
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cverde.co.mz')
REQUIRE_EMAIL_VERIFICATION = config("REQUIRE_EMAIL_VERIFICATION", default=True, cast=_parse_debug)
REQUIRE_PRODUCER_VERIFICATION = config("REQUIRE_PRODUCER_VERIFICATION", default=False, cast=_parse_debug)

# ========== SESSION SETTINGS ==========
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# ========== AUTH SECURITY ==========
# RNF10/RNF11 (SRS): registar tentativas e bloquear após 5 falhas.
MAX_LOGIN_ATTEMPTS = config("MAX_LOGIN_ATTEMPTS", default="5", cast=lambda v: int(v))
ACCOUNT_LOCK_MINUTES = config("ACCOUNT_LOCK_MINUTES", default="15", cast=lambda v: int(v))

# ========== CHECKOUT / SHIPPING ==========
# Regras de negócio (SRS): portes grátis para compras >= 50€.
FREE_SHIPPING_THRESHOLD_EUR = config("FREE_SHIPPING_THRESHOLD_EUR", default="50", cast=lambda v: float(v))
DEFAULT_SHIPPING_COST_EUR = config("DEFAULT_SHIPPING_COST_EUR", default="5", cast=lambda v: float(v))
VAT_RATE = config("VAT_RATE", default="0", cast=lambda v: float(v))  # ex.: 0.23

# ========== SECURITY SETTINGS (production only) ==========
# Para evitar redirecionamentos/headers agressivos em ambientes de testes/DEV,
# estas opções só são ativadas quando explicitamente pedido.
ENABLE_SECURE_SETTINGS = config("ENABLE_SECURE_SETTINGS", default=False, cast=_parse_debug)
if not DEBUG and ENABLE_SECURE_SETTINGS:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_REFERRER_POLICY = 'same-origin'

# ========== LOGGING CONFIGURATION ==========
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ========== MESSAGE TAGS (para compatibilidade com Bulma) ==========
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.WARNING: 'warning',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
}
