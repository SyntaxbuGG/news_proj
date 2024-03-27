from rest_framework import viewsets, status
from django.contrib.auth.models import User, Group
from . import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializerSimple
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Получаем пользователя, которого пытаются изменить
        user_to_update = self.get_object()

        if not request.user.is_superuser:
            if request.user != user_to_update:
                return Response({'errors': "You don't have permission to update this user."},
                                status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if not request.user.is_superuser:
            if request.user != user_to_delete:
                return Response({'errors': "You don't have permission to delete this user."},
                                status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)


