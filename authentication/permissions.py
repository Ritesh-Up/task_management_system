from rest_framework import permissions
from user.models import UserModel

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.user_role == UserModel.USER_ROLE_CHOICES.admin else False