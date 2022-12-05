from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """Доступ только для администратора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ администратору или на чтение без токена."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Доступ на чтение без токена.
    На создание, редактирование и удаление автору, модератору, админу.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_superuser
            or request.user.is_admin
        )


class IsUser(permissions.BasePermission):
    """Доступ к своей учетной записи."""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_user
                or request.user.is_moderator
            )
        )
