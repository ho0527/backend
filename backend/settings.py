from pathlib import Path
import os

BASE_DIR=Path(__file__).resolve().parent.parent

SECRET_KEY="django-insecure-a^w*952yu65u@npg-7-alzonm#0$y$#9+h#5gmlsvv7=v^46s4"

DEBUG=True

ALLOWED_HOSTS=["*"]

INSTALLED_APPS=[
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_yasg"
]

MIDDLEWARE=[
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
	"corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF="backend.urls"


TEMPLATES=[
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,"template")],
        "APP_DIRS": False,
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

WSGI_APPLICATION="backend.wsgi.application"

DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS=[
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
    }
]

LANGUAGE_CODE="en-us"

TIME_ZONE="UTC"

USE_I18N=True

USE_TZ=True

STATIC_URL="static/"

DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"

CSRF_COOKIE_SECURE=False
CSRF_COOKIE_HTTPONLY=False

GRAPHENE={
    "SCHEMA": "django_root.schema.schema"
}

SWAGGER_SETTINGS={
    "DEFAULT_AUTO_SCHEMA_CLASS": "backend.config.swagger.CustomSwaggerAutoSchema",
}

MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"upload")

CORS_URLS_REGEX = r"^.*$"