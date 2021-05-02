from rest_framework import permissions


# TODO оставить, если будут ещё пермишены для readonly
# class BaseCheckReadOnly(permissions.BasePermission):
#     """
#     Object-level permission abstraction to allow readonly requests and do nothing for others.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True


class IsAuthorOrCurrentUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow readonly requests and allow only author of an object to edit it, or edit yourself.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        if obj.hasattr('author'):
            return obj.author == request.user

        # Or trying to edit yourself
        return obj == request.user


class ReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only readonly requests.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # And reject any other
        return False
