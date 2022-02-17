from rest_framework import permissions


class IsMaintainer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_instructor or request.user.is_staff:
            return True
        else:
            return False