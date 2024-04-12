from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


from news_app import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

from ...models import Like


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    # permission_classes = [IsAuthenticated]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializers
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication,SessionAuthentication,BasicAuthentication]

    @action(detail=True, methods=['post'])
    def like_blog(self, request, pk=None):
        news = self.get_object()
        user = request.user

        # Проверяем, поставил ли пользователь уже лайк
        if Like.objects.filter(user=user, blog=news).exists():
            raise ValidationError("You have already liked this blog.")

        # Создаем запись о лайке
        Like.objects.create(user=user, blog=news)
        news.like += 1
        news.save()

        return Response({'status': 'Blog liked'}, status=status.HTTP_200_OK)
