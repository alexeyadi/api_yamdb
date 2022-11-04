from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from reviews.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes
