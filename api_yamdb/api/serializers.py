from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(ModelSerializer):
    """Сериалайзер для юзера."""
    username = CharField(validators=[UniqueValidator(
        queryset=User.objects.all())],
        required=True,
    )
    email = EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio'
                  )

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('You can not use "me"!')
        return username


class CreateUserSerializer(ModelSerializer):
    """Сериалайзер для создания юзера."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio')
        read_only_fields = ('role',)


class SignUpSerializer(ModelSerializer):
    """Сериалайзер для регистрации."""
    username = CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('You can not use "me"!')
        return username

    class Meta:
        model = User
        fields = ("username", "email")


class JWTTokenSerializer(Serializer):
    """Сериалайзер JWT токена."""
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(ModelSerializer):
    """Сериалайзер для жанров произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(ModelSerializer):
    """Сериалайзер для категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(ModelSerializer):
    """Сериалайзер для Произведения, к которым пишут отзывы"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(ModelSerializer):
    """Сериалайзер для Произведения, к которым пишут отзывы"""
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    """Сериалайзер для отзывов на произведения."""
    title = SlugRelatedField(
        slug_field='name', read_only=True
    )
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    """Сериалайзер для комментариев к отзывам."""
    review = SlugRelatedField(
        slug_field='text', read_only=True
    )
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
