from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User


@register(User)
class MyUserAdmin(UserAdmin):
    """Для модели пользователей включена фильтрация по имени и email."""
    list_filter = ("email", "username")
