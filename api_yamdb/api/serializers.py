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


class CreateUserSerializer(ModelSerializer):
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
        fields = ("username", "email")
        model = User


class JWTTokenSerializer(Serializer):
    """Сериалайзер JWT токена."""
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(ModelSerializer):
    """Сериалайзер для отзывов на произведения."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date',)
        # fields = '__all__'
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
        # fields = ('id', 'author', 'review', 'text', 'pub_date',)
        fields = '__all__'
        model = Comment


class GenreSerializer(ModelSerializer):
    """Сериалайзер для жанров произведений"""

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(ModelSerializer):
    """Сериалайзер для категорий произведений"""

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


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
