from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core import mail
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken 

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, UserTokenSerializer
from .confirmation_code import ConfirmationCodeGenerator
from .permissions import IsAdminOnly, IsUser

confirmation_code_generator = ConfirmationCodeGenerator()


@api_view(http_method_names=['POST'])
def send_mail(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = User.objects.create(
            email=request.data.get('email'),
            username=request.data.get('username'),
        )

        if request.data.get('username') == 'me':
            return Response(
                'Выберите другое имя пользователя!',
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_staff = False
        user.set_unusable_password()
        user.save()
        confirmation_code = confirmation_code_generator.make_token(user)
        mail_subject = 'Активация Вашего аккаунта.'
        message = (
            f"Приветствуем! Вот Ваш код: "
            f"{confirmation_code}"
        )
        to_email = str(request.data.get('email'))
        # email = mail.EmailMessage(mail_subject, message, to=[to_email])
        with mail.get_connection() as connection:
            mail.EmailMessage(
                mail_subject, message, to=[to_email],
                connection=connection,
            ).send()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
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
        user = get_object_or_404(User, username=request.user.username)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request},
            )

            if user.role == 'user':
                serializer = UserUpdateSerializer(
                    user,
                    data=request.data,
                    partial=True,
                    context={'request': request},
                )

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)
        serializer = UserSerializer(user)
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
        return Response({'access': str(token),})

    return Response(
        'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
    )
