from rest_framework.permissions import SAFE_METHODS, BasePermission

ROLES_FOR_MODIFY = (
    'moderator',
    'admin',
)


class IsAdminOrReadOnly(BasePermission):
    '''Ограничение на активные действия с объектом.'''
    '''Eсли пользователь не является админом.'''
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated and (
                        request.user.is_admin or request.user.is_superuser
                ))


class IsAdminModeratorAuthorPermission(BasePermission):
    '''Ограничение на активные действия с объектом.'''
    '''Eсли пользователь не является автором, модератором, админом.'''
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role in ROLES_FOR_MODIFY
                )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff)
