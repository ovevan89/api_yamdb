from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or not request.user.is_anonymous
                and request.user.is_administrator())

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (not request.user.is_anonymous
                    and request.user.is_administrator())
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_administrator() or request.user.is_superuser


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method not in permissions.SAFE_METHODS:
        #     return request.user.is_moderator or obj.author == request.user
        # return
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_moderator()
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
