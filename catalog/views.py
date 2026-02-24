"""
Контроллеры приложения catalog.

Отображают главную страницу и страницу контактов с формой обратной связи.
"""

import logging
import re

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger("catalog")

# Простая проверка формата email (базовая).
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_contact_form(name: str, email: str, message: str) -> list[str]:
    """Проверяет поля формы контактов. Возвращает список ошибок (пустой при успехе)."""
    errors = []
    if not name or len(name) < 2:
        errors.append("Имя должно содержать не менее 2 символов.")
    if not email:
        errors.append("Укажите email.")
    elif not EMAIL_RE.match(email):
        errors.append("Некорректный формат email.")
    if not message or len(message.strip()) < 10:
        errors.append("Сообщение должно содержать не менее 10 символов.")
    return errors


def home(request: HttpRequest) -> HttpResponse:
    """
    Контроллер домашней страницы.

    Args:
        request: HTTP-запрос.

    Returns:
        Ответ с отрендеренным шаблоном главной страницы.
    """
    logger.debug("Открыта главная страница")
    return render(request, "catalog/home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Контроллер страницы контактов.

    Обрабатывает GET (показ формы) и POST (отправка формы обратной связи).
    Валидирует поля; при ошибках возвращает форму с сообщениями об ошибках.

    Args:
        request: HTTP-запрос.

    Returns:
        Ответ с шаблоном контактов или сообщением об успешной отправке.
    """
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        errors = _validate_contact_form(name, email, message)
        if errors:
            logger.warning("Ошибки валидации формы контактов: %s", errors)
            return render(
                request,
                "catalog/contacts.html",
                {
                    "success": False,
                    "errors": errors,
                    "submitted_name": name,
                    "submitted_email": email,
                    "submitted_message": message,
                },
            )

        logger.info("Форма контактов отправлена: name=%s, email=%s", name, email)
        return render(
            request,
            "catalog/contacts.html",
            {
                "success": True,
                "submitted_name": name,
            },
        )

    return render(request, "catalog/contacts.html")
