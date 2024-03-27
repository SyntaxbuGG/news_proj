from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

User = get_user_model()


class UserRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Хэшируем пароль перед сохранением
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_login', 'date_joined', ]
