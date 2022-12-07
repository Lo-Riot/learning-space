from rest_framework import permissions
from account.models import Author
from loguru import logger


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == Author.objects.get(user_id=request.user)
