from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            print("permissions/IsAuthorOrReadOnly/has_object_permissions/SAFE_METHODS")
            return True

        # Write permissions are only allowed to the owner of the object.
        print("permissions/IsAuthorOrReadOnly/has_object_permissions/Equalize")

        return hasattr(obj, 'author') and obj.author == request.user
