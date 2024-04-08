from django.urls import path, include

from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/<int:pk>/update_password/', views.UserViewSet.as_view({'put': 'update_password'}), name='update-password'),

]
