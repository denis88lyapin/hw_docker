import json

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status

from users.models import User
from users.permissions import IsUserOrSuperuser
from users.serializers import UserSerializer, UserPublicSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOrSuperuser]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserPublicSerializer
        elif (self.action in ['retrieve', 'update', 'partial_update', 'destroy'] and
              self.request.user == self.get_object() or self.request.user.is_superuser):
            return UserSerializer
        elif self.action == 'retrieve' and self.request.user != self.get_object():
            return UserPublicSerializer
        elif self.action == 'create':
            return UserCreateSerializer


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            instance = self.get_queryset().get(email=response.data['email'])
            password = request.data.get('password')
            if password:
                instance.set_password(password)
                instance.save()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        instance = self.get_object()
        new_password = request.data.get('password')
        if new_password:
            instance.set_password(new_password)
            instance.save()
        return response


