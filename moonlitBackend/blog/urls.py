from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CategoryViewSet, TagsViewSet, ImageViewSet


router = routers.DefaultRouter()

router.register(r'images', ImageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'posts', PostViewSet)

urlpatterns =[
    path('', include(router.urls))
]
