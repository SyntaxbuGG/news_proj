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
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone','email']
        extra_kwargs = {'id': {'read_only': True},'username':{'required':False}, 'phone': {'required': False}}

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
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['url','id','username', 'phone', 'email', 'last_login', 'date_joined']
        read_only_fields = ['id','last_login', 'date_joined']
