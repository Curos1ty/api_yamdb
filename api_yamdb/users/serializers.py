from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для me пользователя."""

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
        read_only_fields = ('role', )


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для токена."""

    class Meta:
        model = User
        fields = [
            'username',
            'confirmation_code'
        ]
