from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class Authenticated(BasePermission):
    def has_permission(self, request: Request, _):

        if not request.user.is_authenticated:
            return False

        return True
