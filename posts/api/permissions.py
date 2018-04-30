from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the author of this post.'

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the author of the 
        post and they are trying to update it.
        """
        my_safe_method = ['GET','PUT']

        if request.method in my_safe_method:
            return True
        return obj.user == request.user
