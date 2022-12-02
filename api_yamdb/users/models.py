from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
        ('django admin', 'django admin')
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
        'Роли',
        max_length=30,
        choices=ROLES,
        default='user'
    )
    is_staff = models.BooleanField('Модератор', default=False)
    is_superuser = models.BooleanField('Джанго администратор', default=False)
    is_admin = models.BooleanField('Администратор', default=False)
    is_active = models.BooleanField('Активная учетная запись', default=True)
    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS: 'list[str]' = ['email']

    class Meta:
        unique_together = ('username', 'email',)