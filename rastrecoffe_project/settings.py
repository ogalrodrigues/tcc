# settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança / Debug
SECRET_KEY = os.getenv("SECRET_KEY", "!!!-defina-no-servidor-!!!")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Hosts e CSRF (Render + outros se necessário)
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "seu-servico.onrender.com"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://seu-servico.onrender.com"
).split(",")

# URL pública para montar QR Codes/links, se você usa isso em templates/modelos
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rastreabilidade.apps.RastreabilidadeConfig",
]

# Middlewares (WhiteNoise antes de SessionMiddleware já está OK)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rastrecoffe_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rastrecoffe_project.wsgi.application"

# Banco de dados (SQLite local; em produção considere Postgres/Render)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Localização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Porto_Velho"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (servem via WhiteNoise)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Arquivos de mídia (uploads/QRs gerados)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Storages (Django 4.2+): agora com 'default' configurado para mídia
STORAGES = {
    "default": {  # <--- ESSENCIAL para FileField/ImageField (QR code etc.)
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Facilitar desenvolvimento local (NÃO use em produção) ---
if os.getenv("RUNNING_LOCALLY", "False").lower() == "true":
    DEBUG = True
    # garante hosts/origens locais mesmo se variáveis de ambiente não estiverem setadas
    local_hosts = {"127.0.0.1", "localhost"}
    ALLOWED_HOSTS = list(set(ALLOWED_HOSTS) | local_hosts)
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]


