from rest_framework.permissions import BasePermission

from school.models import Lesson, Course


class IsModeratorViewSet(BasePermission):
    message = "У Вас не достаточно прав для доступа!"

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators').exists():
            if request.method in ['GET', 'PUT', 'PATCH', 'OPTIONS', 'HEAD']:
                return True
        return False


class IsModerator(BasePermission):
    message = "У Вас не достаточно прав для доступа!"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwnerOrSuperuser(BasePermission):
    message = "Вы не являетесь владельцем!"

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Lesson) or isinstance(obj, Course):
            if request.user == obj.owner or request.user.is_superuser:
                return True
            return False
        else:
            if request.user == obj.user or request.user.is_superuser:
                return True
            return False
