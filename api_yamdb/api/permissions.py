from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or not request.user.is_anonymous and
                request.user.is_administrator())

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (not request.user.is_anonymous and
                    request.user.is_administrator())
        return True
