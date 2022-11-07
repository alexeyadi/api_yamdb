from rest_framework.validators import UniqueValidator
from reviews.models import User

from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        SlugRelatedField, ValidationError,
                                        CharField, EmailField, Serializer)
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
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


class JWTTokenSerializer(Serializer):
    """Сериалайзер JWT токена."""
    username = CharField()
    confirmation_code = CharField()


class ReviewSerializer(ModelSerializer):
    """Сериалайзер для отзывов на произведения."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        # fields = ('id', 'author', 'title', 'text', 'score', 'pub_date',)
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('user', 'title')
            )
        ]


class CommentSerializer(ModelSerializer):
    """Сериалайзер для комментариев к отзывам."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GenreSerializer(ModelSerializer):
    """Сериалайзер для жанров произведений"""

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(ModelSerializer):
    """Сериалайзер для категорий произведений"""

    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(ModelSerializer):
    """Сериалайзер для Произведения, к которым пишут отзывы"""
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug',
        many=True)
    rating = IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
