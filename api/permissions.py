from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True

class IsModeratorUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'moderator':
            return True
