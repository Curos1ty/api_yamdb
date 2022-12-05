from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN_ROLE = 'admin'
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ROLES = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin'),
    )
    username = models.TextField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    first_name = models.TextField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.TextField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роли',
        max_length=150,
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=10,
        blank=True
    )
    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS: 'list[str]' = ['email']

    class Meta:
        unique_together = ('username', 'email',)
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE
