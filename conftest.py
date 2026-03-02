"""Конфигурация pytest и pytest-django."""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def pytest_configure(config):
    """Инициализация Django для pytest (подключение настроек и приложений)."""
    import django

    django.setup()
