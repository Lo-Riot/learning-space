from rest_framework import permissions
from account.models import Creator
from loguru import logger


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == Creator.objects.get(user_id=request.user)
