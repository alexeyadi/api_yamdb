from django.urls import include, path

from rest_framework.routers import DefaultRouter

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#    TokenVerifyView,
#)

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, sign_up)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename=r'reviews'
                   )
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename=r'comments')
v1_router.register('categories', CategoryViewSet, basename='сategories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # TODO: create user with Simple JWT
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', sign_up, name='signup'),
]
