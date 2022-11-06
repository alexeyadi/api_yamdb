from rest_framework.serializers import IntegerField, ModelSerializer, SlugRelatedField, ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio',)


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

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать имя "me"!')
        return username


class ReviewSerializer(ModelSerializer):
    """Сериалайзер для отзывов на произведения."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
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
