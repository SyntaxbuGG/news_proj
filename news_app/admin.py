from django.contrib import admin
from . import models


# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = models.Image


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    fields = ['title','subtitle','content','author','category','tags','created_at','updated_at']
    list_display = ['created_at','updated_at','author']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageAdmin]


admin.site.register(models.Category)
admin.site.register(models.Tag)