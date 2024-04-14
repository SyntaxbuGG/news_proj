from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from rest_framework import viewsets, status, filters

from . import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'phone', 'email']

    def get_permissions(self):
        if self.action in ['delete']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        # Проверяем тип запроса и возвращаем соответствующий сериализатор
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return serializers.UserRegSerializer
        else:
            return serializers.UserSerializer

    @swagger_auto_schema(request_body=serializers.UserRegSerializer)
    def create(self, request, *args, **kwargs):
        serializer = serializers.UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Обновление информации о пользователе",
        request_body=serializers.UserRegSerializer,

    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        #     # Получаем пользователя, которого пытаются изменить
        #     user_to_update = self.get_object()
        #
        #     if not request.user.is_superuser:
        #         if request.user != user_to_update:
        #             return Response({'errors': "You don't have permission to update this user."},
        #                             status=status.HTTP_403_FORBIDDEN)
        #


    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if not request.user.is_superuser:
            if request.user != user_to_delete:
                return Response({'errors': "You don't have permission to delete this user."},
                                status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(request_body=serializers.UserChangePassword)
    def update_password(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.UserChangePassword(user, data=request.data)
        if serializer.is_valid():
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if not old_password:
                return Response({'error': 'Old password is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not check_password(old_password, user.password):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
