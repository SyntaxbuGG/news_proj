from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

User = get_user_model()


class UserChangePassword(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone', 'email']
        extra_kwargs = {'id': {'read_only': True}, 'username': {'required': False}, 'phone': {'required': False}}

    def create(self, validated_data):
        validated_data['username'] = self.initial_data.get('username')
        validated_data['password'] = self.initial_data.get('password')

        # Проверяем наличие обязательных полей при создании
        if not validated_data['username'] and not validated_data['password']:
            raise serializers.ValidationError("Username and password are required for creating a new user")

        # Создаем пользователя
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Устанавливаем новый пароль, если он передан
        if password is not None:
            instance.set_password(password)

        # Сохраняем пользователя
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'phone', 'email', 'last_login', 'date_joined']
        read_only_fields = ['id', 'last_login', 'date_joined']
