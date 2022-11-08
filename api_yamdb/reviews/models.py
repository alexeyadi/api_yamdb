from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validation_year

# TODO Моя версия
USER = 'user'
MODER = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    """"Пользователь."""
    # USER = 'user' TODO Вернуть - исходная версия
    # MODER = 'moderator' TODO Вернуть - исходная версия
    # ADMIN = 'admin' TODO Вернуть - исходная версия
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
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        # return self.role == self.MODER TODO Вернуть - исходная версия
        return self.role == MODER  # TODO Моя версия

    @property
    def is_admin(self):
        # return self.role == self.ADMIN TODO Вернуть - исходная версия
        return self.role == ADMIN # TODO Моя версия

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # TODO Уточнить, нужно ли
    def __str__(self):
        return self.username


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256, verbose_name='Имя жанра')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""
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


class Review(models.Model):
    """Отзывы на произведения."""
    # title_id = models.IntegerField(
    #     Title.pk,
    #     related_name='reviews',
    #     verbose_name='Id произведения'
    # )
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
    score = models.IntegerField(
        blank=False,
        validators=[
            MinValueValidator(1, message='Значение меньше минимального. Значение должно быть от 1 до 10'),
            MaxValueValidator(10, message='Значение больше максимального. Значение должно быть от 1 до 10'),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        # db_table = 'review_comment'
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
        #         #fields=['author', title.title._check_id_field()], name='unique_review' TODO Убрать, если вариант ниже сработает
                fields=['author', 'title'], name='unique_review',
            )
        ]

    def __str__(self):
        return self.text[:10]


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
        return self.text[:10]


