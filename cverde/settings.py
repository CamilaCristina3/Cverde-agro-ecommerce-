"""
COVERDE - cverde/settings.py
Configurações principais do projeto.
"""

from pathlib import Path
from decouple import config, Csv


# =====================================================
# BASE DIR
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SEGURANÇA / DEBUG
# =====================================================

SECRET_KEY = config("SECRET_KEY", default="change-me-dev-coverde")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,testserver",
    cast=Csv()
)


# =====================================================
# APPS INSTALADAS
# =====================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps COVERDE
    "apps.users_auth",
    "apps.users",
    "apps.categories",
    "apps.producers",
    "apps.stores",
    "apps.products",
    "apps.cart",
    "apps.orders",
    "apps.payments",
    "apps.deliveries",
    "apps.reviews",
    "apps.support",
    "apps.inventory",
    "apps.reports",
    "apps.notifications",
    "apps.pages",
    "apps.chat",
]


# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =====================================================
# URLS / WSGI / ASGI
# =====================================================

ROOT_URLCONF = "cverde.urls"

WSGI_APPLICATION = "cverde.wsgi.application"

ASGI_APPLICATION = "cverde.asgi.application"


# =====================================================
# TEMPLATES
# =====================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =====================================================
# BASE DE DADOS
# =====================================================

DB_USE_SQLITE = str(
    config("DB_USE_SQLITE", default="false")
).strip().lower() in ("1", "true", "yes", "on")

if DB_USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": config("DB_NAME", default="coverde_db"),
            "USER": config("DB_USER", default="root"),
            "PASSWORD": config("DB_PASSWORD", default="0000"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }


# =====================================================
# MODELO DE UTILIZADOR
# =====================================================

AUTH_USER_MODEL = "users_auth.User"


# =====================================================
# PASSWORD VALIDATION
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =====================================================
# INTERNACIONALIZAÇÃO
# =====================================================

LANGUAGE_CODE = "pt-pt"

TIME_ZONE = "Europe/Lisbon"

USE_I18N = True

USE_TZ = True


# =====================================================
# STATIC / MEDIA
# =====================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =====================================================
# DEFAULT PRIMARY KEY
# =====================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================================
# LOGIN / LOGOUT
# =====================================================

LOGIN_URL = "users:login"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# =====================================================
# EMAIL
# =====================================================

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
)

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="noreply@coverde.pt"
)

SUPPORT_EMAIL = config("SUPPORT_EMAIL", default="suporte@coverde.pt")
ACCOUNT_ACTIVATION_TOKEN_HOURS = config("ACCOUNT_ACTIVATION_TOKEN_HOURS", default=48, cast=int)


# =====================================================
# PAGAMENTO DE TESTE (DESENVOLVIMENTO)
# =====================================================

PAYMENT_TEST_PASSWORD = config("PAYMENT_TEST_PASSWORD", default="1234")
PAYMENT_TEST_SIGNATURE = config("PAYMENT_TEST_SIGNATURE", default="COVERDE-TEST")


# =====================================================
# SEGURANÇA DE CONTA
# =====================================================

MAX_LOGIN_ATTEMPTS = config("MAX_LOGIN_ATTEMPTS", default=5, cast=int)

ACCOUNT_LOCK_MINUTES = config("ACCOUNT_LOCK_MINUTES", default=15, cast=int)


# =====================================================
# ENVIO / IVA
# =====================================================

FREE_SHIPPING_THRESHOLD_EUR = config(
    "FREE_SHIPPING_THRESHOLD_EUR",
    default=50,
    cast=float
)

DEFAULT_SHIPPING_COST_EUR = config(
    "DEFAULT_SHIPPING_COST_EUR",
    default=5,
    cast=float
)

VAT_RATE = config("VAT_RATE", default=0.06, cast=float)