from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == User.ADMIN

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == User.ADMIN


class IsAdminOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
                request.user.is_staff or request.user.role == User.ADMIN)
                )


class IsModeratorAdminAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and (
                request.user.role == User.MODERATOR or request.user.is_staff
                or request.user.role == User.ADMIN or obj.author == request.user)
                or request.method in permissions.SAFE_METHODS
                )


class IsAdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.role == User.ADMIN)
