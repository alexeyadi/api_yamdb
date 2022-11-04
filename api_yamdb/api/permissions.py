from rest_framework.permissions import BasePermission, SAFE_METHODS


ROLES_FOR_MODIFY = (
    'moderator',
    'admin',
)


class IsAuthorPermission(BasePermission):
    '''Ограничение на активные действия с объектом, если пользователь не является автором, модератором, админом.'''
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user or request.user.role in ROLES_FOR_MODIFY)
