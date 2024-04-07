from drf_yasg import openapi
from rest_framework import viewsets, status,filters

from . import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username','phone','email']

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'update', 'delete']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @swagger_auto_schema(request_body=serializers.UserRegSerializer)
    def create(self, request, *args, **kwargs):
        serializer = serializers.UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Обновление информации о пользователе",
        request_body=serializers.UserSerializer,

    )
    def update(self, request, *args, **kwargs):
        # Получаем пользователя, которого пытаются изменить
        user_to_update = self.get_object()

        if not request.user.is_superuser:
            if request.user != user_to_update:
                return Response({'errors': "You don't have permission to update this user."},
                                status=status.HTTP_403_FORBIDDEN)

        # Добавляем примеры данных в Swagger схему
        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if not request.user.is_superuser:
            if request.user != user_to_delete:
                return Response({'errors': "You don't have permission to delete this user."},
                                status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
