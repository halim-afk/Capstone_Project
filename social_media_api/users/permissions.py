from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read permissions are allowed to any request.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        # obj is assumed to be an instance of a model with a 'user' attribute (like Post)
        # OR the obj itself is a User instance (like for UserProfileViewSet).
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
