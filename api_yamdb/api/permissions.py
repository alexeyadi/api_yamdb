from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorPermission(BasePermission):
    '''Ограничение на активные действия с объектом, если пользователь не является автором.'''
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
