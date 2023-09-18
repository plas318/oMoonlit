from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import PostSerializer
# Create your views here.

class ThreadsViewSet(viewsets.ModelViewSet):
    pass

# get, post, put, patch, delete is the original crud
class PostsViewSet(viewsets.ModelViewSet):
    # Viewsets updated crud
    def create():
        pass
    def update():
        pass
    def partial_update():
        pass
    def destroy():
        pass

class CommentsViewSet(viewsets.ModelViewSet):
    pass

class TagsViewSet(viewsets.ModelViewSet):
    pass
class LikesViewSet(viewsets.ModelViewSet):
    pass
class DisLikesViewSet(viewsets.ModelViewSet):
    pass



