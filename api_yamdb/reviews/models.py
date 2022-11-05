from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (MODER, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True)
    email = models.EmailField(
        verbose_name='Почта',
        unique=True, )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True)
    role = models.CharField(
        verbose_name='Права доступа',
        choices=ROLES,
        default='user',
        max_length=50)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,)

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


def __str__(self):
    return self.username
