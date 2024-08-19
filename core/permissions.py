from rest_framework.permissions import BasePermission


class StaffAllowedPermission(BasePermission):
    def has_permission(self, request, view):
        staff_allowed_http = ['POST', 'GET', 'PUT', 'PATCH']
        if request.user.is_staff:
            return request.method in staff_allowed_http

        return request.user.is_manager