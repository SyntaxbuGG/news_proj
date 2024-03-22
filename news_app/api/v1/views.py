from rest_framework import viewsets
from news_app import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication]

