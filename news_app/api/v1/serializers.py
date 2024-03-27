from rest_framework import serializers
from news_app import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']


class NewsSerializers(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    like = serializers.SerializerMethodField(read_only=True)


    def get_author(self, obj):
        return obj.author.username

    def get_like(self, obj):
        return obj.like.count()



    class Meta:
        model = models.News
        fields = ['url', 'title', 'subtitle', 'content', 'author', 'category', 'tags', 'like', 'created_at',
                  'updated_at',
                  'images']
