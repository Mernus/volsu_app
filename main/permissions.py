from rest_framework import permissions


class BaseCheckReadOnly(permissions.BasePermission):
    """
    Object-level permission abstraction to allow readonly requests and do nothing for others.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True


class IsAuthorOrReadOnly(BaseCheckReadOnly):
    """
    Object-level permission to allow readonly requests and allow only author of an object to interact.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        super(IsAuthorOrReadOnly, self).has_object_permission(request, view, obj)

        # If user is author of object.
        return obj.author == request.user


class IsCurrentUser(permissions.BasePermission):
    """
    Object-level permission to allow to interact only if object is requested user.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class ReadOnly(BaseCheckReadOnly):
    """
    Object-level permission to allow only readonly requests.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        super(ReadOnly, self).has_object_permission(request, view, obj)

        # And reject any other
        return False
