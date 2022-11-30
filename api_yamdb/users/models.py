from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    username = models.TextField(
        'Имя пользователя',
        max_length=20,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    first_name = models.TextField(
        'Имя',
        max_length=30,
        blank=True,
    )
    last_name = models.TextField(
        'Фамилия',
        max_length=30,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default='user'
    )
    is_user = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS: 'list[str]' = ['email']

    class Meta:
        unique_together = ('username', 'email',)