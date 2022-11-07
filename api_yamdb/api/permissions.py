from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    '''Ограничение на активные действия с объектом, если пользователь не является админом.'''
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_admin or request.user.is_superuser)


class IsAdminUserPermission(BasePermission):
    '''Ограничение на активные действия с объектом, если пользователь не является юзером или админом.'''
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin)


class IsAdminModeratorAuthorPermission(BasePermission):
    '''Ограничение на активные действия с объектом, если пользователь не является автором, модератором, админом.'''
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role in ROLES_FOR_MODIFY)
