from rest_framework import permissions


class IsAdminOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and (request.user.is_staff or request.user.role == 'admin')
        )


class IsModeratorAdminAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_authenticated
                and (request.user.role == 'moderator'
                or request.user.is_staff or request.user.role == 'admin'
                or obj.author == request.user)
                or request.method in permissions.SAFE_METHODS
        )


class IsAdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and (request.user.is_staff or request.user.role == 'admin')
                or request.method in permissions.SAFE_METHODS
        )