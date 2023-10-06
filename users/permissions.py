from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserOrSuperuser(BasePermission):
    message = "У Вас не достаточно прав для доступа!"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user == view.get_object() or request.user.is_superuser:
            return True
        return False
