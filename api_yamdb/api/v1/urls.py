from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    sign_up)

app_name = 'api_v1'

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename=r'reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename=r'comments'
)
v1_router.register('categories', CategoryViewSet, basename='сategories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')


jwtpatterns = [
    path('token/', get_jwt_token, name='token_obtain_pair'),
    path('signup/', sign_up, name='signup'),
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(jwtpatterns)),
]
