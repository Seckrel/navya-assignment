from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager
