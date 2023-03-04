from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a author, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
