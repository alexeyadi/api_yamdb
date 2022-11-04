from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comment, Review, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields =


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
