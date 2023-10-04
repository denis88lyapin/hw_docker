from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer, UserPublicSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserPublicSerializer
        elif (self.action in ['retrieve', 'update', 'partial_update'] and self.request.user == self.get_object() or
              self.request.user.is_superuser):
            return UserSerializer
        elif self.action == 'retrieve' and self.request.user != self.get_object():
            return UserPublicSerializer
        elif self.action == 'create':
            return UserSerializer
        elif self.action == 'destroy' and self.request.user == self.get_object() or self.request.user.is_superuser:
            return UserSerializer
