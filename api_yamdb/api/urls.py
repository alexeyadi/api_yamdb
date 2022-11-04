from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.views import (
    CommentViewSet,
    ReviewViewSet, UserViewSet
)


app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename=r'reviews'
                )
v1_router.register(r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/',
                CommentViewSet, basename=r'comments'
                )



urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]