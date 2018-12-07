from rest_framework.permissions import BasePermission

class IsCurrentUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        print (request.url)
        return request.user and request.user.is_authenticated