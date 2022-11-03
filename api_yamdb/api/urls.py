from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    ReviewViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename=r'reviews'
                )
router.register(r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/',
                CommentViewSet, basename=r'comments'
                )
