from pathlib import Path
import os
import dj_database_url

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Segurança / Ambiente ===
SECRET_KEY = os.getenv("SECRET_KEY", "!!!-defina-no-servidor-!!!")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "projeto-tcc-rastreabilidade.onrender.com"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://projeto-tcc-rastreabilidade.onrender.com"
).split(",")

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

# Quando atrás de proxy (Render) para que request.is_secure() funcione
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"

# === Apps ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rastreabilidade.apps.RastreabilidadeConfig",
]

# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static via WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# === URLs / WSGI ===
ROOT_URLCONF = "rastrecoffe_project.urls"
WSGI_APPLICATION = "rastrecoffe_project.wsgi.application"

# === Templates ===
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

# === Banco de Dados ===
# Local: SQLite (fallback)
# Produção (Render): usar DATABASE_URL (PostgreSQL)
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=True,
    )
}

# === Internacionalização ===
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Porto_Velho"
USE_I18N = True
USE_TZ = True

# === Arquivos Estáticos e de Mídia ===
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"          # coletados no deploy
STATICFILES_DIRS = [BASE_DIR / "static"]        # seus assets de app

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"                 # uploads (ex.: QR codes)

# Django 5+: defina 'default' e 'staticfiles' em STORAGES
STORAGES = {
    # Onde salvar arquivos de usuário (FileField/ImageField), ex.: QR code
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": str(MEDIA_ROOT),
            "base_url": MEDIA_URL,
        },
    },
    # Arquivos estáticos servidos por WhiteNoise com hash no nome
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# === Outros ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Logging básico (útil para erros 500 no Render) ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
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
    SECURE_SSL_REDIRECT = False
