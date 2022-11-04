
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CommentSerializer, ReviewSerializer, UserSerializer

from .permissions import IsAuthorPermission
from reviews.models import Title, User


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorPermission
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer): #ToDO Make correct validation
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # if Review.objects.filter(user=self.request.user):
        #         raise ValidationError('Пользователь может оставить только один отзыв на произведение.')
        #     return serializer.save(author=self.request.user, title=title)
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorPermission
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes

