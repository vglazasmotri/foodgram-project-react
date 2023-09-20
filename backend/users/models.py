from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Модель кастомного пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
