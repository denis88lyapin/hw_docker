from django.utils import timezone
from users.models import User


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=request.user.pk)
                user.last_login = timezone.now()
                user.save()
            except User.DoesNotExist:
                pass

        return response
