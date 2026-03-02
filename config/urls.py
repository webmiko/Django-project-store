"""
Маршрутизация URL проекта config.

Список urlpatterns связывает URL с представлениями.
Документация: https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
]
