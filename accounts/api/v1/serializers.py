from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

User = get_user_model()


class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_login', 'date_joined']

