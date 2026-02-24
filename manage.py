#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""

import os
import sys


def main():
    """Запуск административных задач."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Установлен ли он и доступен ли в "
            "переменной окружения PYTHONPATH? Не забудьте активировать виртуальное окружение."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
