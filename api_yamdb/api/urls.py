from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # TODO: create user with Simple JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/signup/', signup, name='signup'),
]