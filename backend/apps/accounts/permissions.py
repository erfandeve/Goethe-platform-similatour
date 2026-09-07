from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    message = "Authentication required."

    def has_permission(self, request, view):
        return bool(getattr(request, "user", None))


class IsStaff(BasePermission):
    """Back-office access. Checked on every admin endpoint, never in the client."""

    message = "Staff access required."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_staff)
