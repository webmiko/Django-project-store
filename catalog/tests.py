"""
Тесты приложения catalog.

Покрывают главную страницу, форму контактов (GET/POST),
валидацию и нестабильные сценарии (пустые данные, неверный email).
"""

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestHomeView:
    """Тесты главной страницы."""

    def test_home_returns_200(self):
        client = Client()
        response = client.get(reverse("catalog:home"))
        assert response.status_code == 200

    def test_home_uses_correct_template(self):
        client = Client()
        response = client.get(reverse("catalog:home"))
        assert "catalog/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestContactsView:
    """Тесты страницы контактов."""

    def test_contacts_get_returns_200(self):
        client = Client()
        response = client.get(reverse("catalog:contacts"))
        assert response.status_code == 200

    def test_contacts_get_shows_form(self):
        client = Client()
        response = client.get(reverse("catalog:contacts"))
        assert b"name" in response.content
        assert b"email" in response.content
        assert b"message" in response.content
        assert response.context.get("success") is not True

    def test_contacts_post_empty_shows_errors(self):
        """POST с пустыми полями не считается успехом, возвращаются ошибки."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {"name": "", "email": "", "message": ""},
        )
        assert response.status_code == 200
        assert response.context["success"] is False
        assert "errors" in response.context
        assert len(response.context["errors"]) > 0

    def test_contacts_post_short_name_shows_error(self):
        """Имя короче 2 символов — ошибка валидации."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {
                "name": "A",
                "email": "user@example.com",
                "message": "Достаточно длинное сообщение для проверки.",
            },
        )
        assert response.status_code == 200
        assert response.context["success"] is False
        errors = response.context.get("errors", [])
        assert any("имя" in e.lower() or "2" in e for e in errors)

    def test_contacts_post_invalid_email_shows_error(self):
        """Некорректный email — ошибка валидации."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {
                "name": "Иван",
                "email": "not-an-email",
                "message": "Достаточно длинное сообщение для проверки.",
            },
        )
        assert response.status_code == 200
        assert response.context["success"] is False
        errors = response.context.get("errors", [])
        assert any("email" in e.lower() for e in errors)

    def test_contacts_post_short_message_shows_error(self):
        """Сообщение короче 10 символов — ошибка."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {
                "name": "Иван",
                "email": "user@example.com",
                "message": "Коротко",
            },
        )
        assert response.status_code == 200
        assert response.context["success"] is False
        errors = response.context.get("errors", [])
        assert any("10" in e or "сообщение" in e.lower() for e in errors)

    def test_contacts_post_valid_shows_success(self):
        """Корректные данные — успешная отправка."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {
                "name": "Иван Петров",
                "email": "ivan@example.com",
                "message": "Достаточно длинное сообщение для проверки формы.",
            },
        )
        assert response.status_code == 200
        assert response.context["success"] is True
        assert response.context.get("submitted_name") == "Иван Петров"

    def test_contacts_post_strips_whitespace(self):
        """Пробелы в начале/конце полей обрезаются."""
        client = Client()
        response = client.post(
            reverse("catalog:contacts"),
            {
                "name": "  Иван  ",
                "email": "  ivan@example.com  ",
                "message": "  Сообщение длиной больше десяти символов.  ",
            },
        )
        assert response.status_code == 200
        assert response.context["success"] is True
        assert response.context.get("submitted_name") == "Иван"


class TestValidateContactForm:
    """Тесты валидатора формы (изолированно)."""

    def test_valid_data(self):
        from catalog.views import _validate_contact_form

        errors = _validate_contact_form("Иван", "a@b.co", "Текст сообщения больше 10 символов.")
        assert errors == []

    def test_empty_name(self):
        from catalog.views import _validate_contact_form

        errors = _validate_contact_form("", "a@b.co", "Текст больше десяти символов.")
        assert any("имя" in e.lower() for e in errors)

    def test_invalid_email(self):
        from catalog.views import _validate_contact_form

        errors = _validate_contact_form("Иван", "invalid", "Текст больше десяти символов.")
        assert any("email" in e.lower() for e in errors)

    def test_short_message(self):
        from catalog.views import _validate_contact_form

        errors = _validate_contact_form("Иван", "a@b.co", "Коротко")
        assert any("10" in e or "сообщение" in e.lower() for e in errors)


class TestSettingsHelpers:
    """Тесты вспомогательных функций настроек (устойчивость к пустым/пробельным значениям)."""

    def test_parse_allowed_hosts_empty(self):
        from config.settings import _parse_allowed_hosts

        assert _parse_allowed_hosts("") == []
        assert _parse_allowed_hosts("   ") == []

    def test_parse_allowed_hosts_strips_and_filters(self):
        from config.settings import _parse_allowed_hosts

        assert _parse_allowed_hosts("localhost, 127.0.0.1") == ["localhost", "127.0.0.1"]
        assert _parse_allowed_hosts("  a  ,  b  ,  ") == ["a", "b"]
