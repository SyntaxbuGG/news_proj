from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

User = get_user_model()


class UserRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password','phone']

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)  # Удаляем phone из validated_data
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if phone:
            user.phone = phone
            user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['url', 'username','phone', 'email', 'last_login', 'date_joined']
        read_only_fields = ['last_login', 'date_joined']


