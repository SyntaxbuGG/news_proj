import os.path

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, unique=True,blank=True,null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    tags = models.ManyToManyField(Tag,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    # slug automatic save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subtitle)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


def image_upload(instance, filename):
    # get id image
    news_id = instance.news.id

    path = os.path.join('news/image', str(news_id), filename)
    return path


class Image(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_upload)
