from rest_framework.serializers import ModelSerializer, ValidationError
from reviews.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio', )

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать имя "me"!')
        return username
