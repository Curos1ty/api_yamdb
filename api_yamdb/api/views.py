from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Review, Title

from users.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrReadOnly
)

from .filters import TitleFilter
from .paginators import CommentPagination, ReviewPagination
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateUpdateSerializer,
    TitleSerializer,
)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Общие настройки для классов c методами post, get, delete."""

    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    """Класс категорий произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Класс жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведений."""

    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


def get_title_or_review(self):
    """Получение title_id или review_id."""
    if 'review_id' in self.kwargs:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review
    title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    return title


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс отзывов."""

    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        return get_title_or_review(self).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=get_title_or_review(self)
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Класс комментариев к отзывам."""

    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        return get_title_or_review(self).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=get_title_or_review(self)
        )
