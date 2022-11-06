from rest_framework.serializers import (
    ModelSerializer, ValidationError, CharField, EmailField, Serializer
)
from rest_framework.validators import UniqueValidator
from reviews.models import User


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
            raise ValidationError('Нельзя использовать имя "me"!')
        return username


class JWTTokenSerializer(Serializer):
    username = CharField()
    confirmation_code = CharField()
