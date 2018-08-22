from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You must be the author of this post.'

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the author of the 
        post and they are trying to update it.
        """
        # my_safe_method = ['GET','PUT']

        # if request.method in my_safe_method:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
