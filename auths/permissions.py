from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return request.user.is_manager


class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_staff
