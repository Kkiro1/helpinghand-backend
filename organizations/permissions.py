from rest_framework.permissions import BasePermission

from accounts.models import UserProfile


class IsOrganizationUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        return bool(profile and profile.role == UserProfile.ROLE_ORGANIZATION)
