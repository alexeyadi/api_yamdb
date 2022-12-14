from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from .validators import validation_year

FIRST_SYMBOLS = 10

USER = 'user'
MODER = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    """"Пользователь."""
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
        default=USER,
        max_length=50)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODER

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256, verbose_name='Имя жанра')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
        validators=[RegexValidator(
            r'^[-a-zA-Z0-9_]+$', message='Не допустимые символы'
        )
        ],
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256, verbose_name='Имя категории')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        validators=[RegexValidator(
            r'^[-a-zA-Z0-9_]+$', message='Не допустимые символы'
        )
        ],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""
    name = models.CharField(max_length=150, verbose_name='Название')
    year = models.PositiveIntegerField(
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
        return self.name[:FIRST_SYMBOLS]


class Review(models.Model):
    """Отзывы на произведения."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(blank=False, verbose_name='Текст отзыва')
    score = models.PositiveIntegerField(
        blank=False,
        validators=[
            MinValueValidator(
                1, message='Значение меньше минимального.'
                'Значение должно быть от 1 до 10'
            ),
            MaxValueValidator(
                10, message='Значение больше максимального.'
                'Значение должно быть от 1 до 10'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review',
            )
        ]

    def __str__(self):
        return self.text[:FIRST_SYMBOLS]


class Comment(models.Model):
    """Комментарии на отзывы."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(blank=False, verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:FIRST_SYMBOLS]
