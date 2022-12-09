from django.core import mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .paginators import CommentPagination, ReviewPagination
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateUpdateSerializer,
    TitleSerializer,
    UserSerializer,
    UserTokenSerializer,
    UserUpdateSerializer
)
from .utils import get_title_or_review
from reviews.models import Category, Genre, Title
from users.confirmation_code import ConfirmationCodeGenerator
from users.models import User
from users.permissions import (
    IsAdminOnly,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrReadOnly,
    IsUser
)

confirmation_code_generator = ConfirmationCodeGenerator()


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

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


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


@api_view(http_method_names=['POST'])
def send_mail(request):
    """Отправка кода подтверждения."""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(
        email=serializer.validated_data.get('email'),
        username=serializer.validated_data.get('username'),
    )
    user.is_staff = False
    user.set_unusable_password()
    user.save()
    confirmation_code = confirmation_code_generator.make_token(user)
    mail_subject = 'Активация Вашего аккаунта.'
    message = (
        f'Приветствуем! Вот Ваш код: '
        f'{confirmation_code}'
    )
    to_email = str(serializer.validated_data.get('email'))

    with mail.get_connection() as connection:
        mail.EmailMessage(
            mail_subject, message, to=[to_email],
            connection=connection,
        ).send()

    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """Вьюсет для пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=(IsUser,)
    )
    def me(self, request):
        """Получение и редактирование аккаунта пользователя."""

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request},
            )

            if request.user.is_user:
                serializer = UserUpdateSerializer(
                    request.user,
                    data=request.data,
                    partial=True,
                    context={'request': request},
                )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
def create_token(request):
    """Получение токена по коду подтверждения."""
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'access': str(token), })

    return Response(
        'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
    )
