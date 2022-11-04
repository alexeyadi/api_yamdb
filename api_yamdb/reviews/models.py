from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validation_year

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


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(max_length=256, verbose_name='Имя жанра')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField(max_length=256, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""
    name = models.CharField(max_length=150, verbose_name='Название')
    year = models.IntegerField(
        validators=(validation_year,),
        verbose_name='Год выпуска')
    description = models.CharField(
        max_length=150,
        blank=True, null=True,
        verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория',
        null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
