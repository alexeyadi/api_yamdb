from rest_framework.serializers import ModelSerializer
from reviews.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio', )
