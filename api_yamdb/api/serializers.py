
from rest_framework.serializers import ModelSerializer, SlugRelatedField, ValidationError, CharField, EmailField, Serializer
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Comment, Review, User


class UserSerializer(ModelSerializer):
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
    username = CharField()
    confirmation_code = CharField()


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
