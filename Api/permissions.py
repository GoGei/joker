from rest_framework.permissions import BasePermission
from core.Utils.Access.user_check_functions import manager_check, superuser_check


class IsStaffUserPermission(BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return manager_check(request.user)


class IsSuperuserPermission(BasePermission):
    """
    Allows access only to superuser users.
    """

    def has_permission(self, request, view):
        return superuser_check(request.user)
