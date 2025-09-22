from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "!!!-defina-no-servidor-!!!")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "seu-servico.onrender.com"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://seu-servico.onrender.com"
).split(",")

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rastreabilidade.apps.RastreabilidadeConfig",
]

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

# ===============================
# CONFIGURAÇÃO DO BANCO POSTGRES
# ===============================
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://db_rastrecoffe_user:SUA_SENHA@SEU_HOST:5432/db_rastrecoffe",
        conn_max_age=600,
        ssl_require=True,
    )
}

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Porto_Velho"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"      
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

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
