"""
Настройки Django для проекта config.

Создано командой django-admin startproject (Django 6.0.1).

Подробнее о настройках:
https://docs.djangoproject.com/en/6.0/topics/settings/
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Корневая директория проекта: BASE_DIR / 'подкаталог'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения из файла .env.
load_dotenv(BASE_DIR / ".env")

# Настройки для разработки; для production см. чеклист развёртывания:
# https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# В production отключайте DEBUG!
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Секретный ключ: из окружения; без него в production — ошибка.
# Для локальной разработки без .env подставляется явно небезопасный ключ.
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-only-change-in-production"
    else:
        raise RuntimeError("Задайте SECRET_KEY в переменных окружения (например в .env)")


def _parse_allowed_hosts(value: str) -> list[str]:
    """Парсит ALLOWED_HOSTS: убирает пробелы и пустые элементы."""
    if not value or not value.strip():
        return []
    return [h.strip() for h in value.split(",") if h and h.strip()]


ALLOWED_HOSTS = _parse_allowed_hosts(os.getenv("ALLOWED_HOSTS", ""))


# Подключённые приложения

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# База данных
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# Если задана переменная DB_NAME — используется PostgreSQL, иначе SQLite для разработки.
if os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "django_store"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }


# Валидаторы паролей
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Интернационализация
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Статические файлы (CSS, JavaScript, изображения)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Медиафайлы (загрузки пользователей)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Логирование
# https://docs.djangoproject.com/en/6.0/topics/logging/
_log_dir = BASE_DIR / "logs"
_log_dir.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(_log_dir / "django.log"),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "catalog": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
