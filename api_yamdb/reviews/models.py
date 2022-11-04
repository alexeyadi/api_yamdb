from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ]


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=CHOICES, default='user', max_length=50)
    bio = models.TextField('Биография', blank=True,)

class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

def __str__(self):
    return self.username
