from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'last_login')



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'password')
        # extra_kwargs = {
        #     'phone': {'required': False},
        #     'city': {'required': False},
        #     'avatar': {'required': False},
        # }



