from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.generics import 
from .models import Post, Category, Tag, Image
from .serializers import PostSerializer, CategorySerializer, TagSerializer, ImageSerializer
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

import os
from django.core.files.base import ContentFile
import base64
from .utils import extract_base64_images, replace_base64_with_urls, get_image_url, generate_random_name

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [IsAuthenticated]  # Allow any user to create
        else:
            permission_classes = [AllowAny]  # Require authentication for other actions
        return [permission() for permission in permission_classes]
    

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [IsAuthenticated]  # Allow any user to create
        else:
            permission_classes = [AllowAny]  # Require authentication for other actions
        return [permission() for permission in permission_classes]
    
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [IsAuthenticated]  # Allow any user to create
        else:
            permission_classes = [AllowAny]  # Require authentication for other actions
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    '''
    Post ViewSet
    
    get: List all post
    get/id: List specified post
    post: Create new post
    put/id: Update specified post
    delete/id: Remove specified post
    '''
    
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'content']
    ordering = ['-created']
    ordering_fields = ['title', 'created']
    search_fields = ['title']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [IsAuthenticated]  # Allow any user to create
        else:
            permission_classes = [AllowAny]  # Require authentication for other actions
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        '''
        creates a new post
        recieves a form data consisting
        title, content(including base64 encoded images), tags(array)
        
        '''
        request_copy = request.data.copy()
        request_copy['author'] = request.user.pk
        tags = request_copy.pop('tags', [])
        tags = tags[0].split(',')
        tag_objects = [Tag.objects.get_or_create(name=name)[0] for name in tags]
        
        ####
        content = request_copy['content'] 
        bs64_images = extract_base64_images(content)
        
        created_images = []
        
        for bs64_image in bs64_images:
            print("base64_images first 10: ", bs64_image[:10])
            print("base64_images last 10: ", bs64_image[-10:-1])
            # create the image object, and receive the object?
            # get the name of the image to get the url of the img
            # replace the url of the content with the url obtained
            # now serialize the post with the replaced content
            # add the post foreignkey to the image object after post is created
            # Decode the img into a file and create image object
            image_data = ContentFile(base64.b64decode(bs64_image), name=f'{generate_random_name(12)}.jpeg')
            created_image = Image.objects.create(image = image_data)
            created_images.append(created_image)
            print('Created image: ', created_image)
            
            image_url = get_image_url(created_image)
            print('image url: ', image_url)
            content = replace_base64_with_urls(content, bs64_image, image_url)
        print('After replacing content with urls: ', content)
            
        request_copy['content'] = content
        
        serializer = self.get_serializer(data=request_copy)
        
        if serializer.is_valid():
            post = serializer.save()
            print(f'{post}')
            print(f'tag_objects: {tag_objects}')
            post.tags.set(tag_objects)
            print(post)
            for image in created_images:
                image.post = post
                image.save()
                
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        
        # First get object from the database
        # Save the changed content accordingly
        # Delete images if they are excluded from the content page;
        
        instance = self.get_object()
        
        
        request_copy = request.data.copy()
        request_copy['author'] = request.user.pk
        print(request.user.pk)
        tags = request_copy.pop('tags', [])
        
        print('tags: ', [tag for tag in tags])
        tags = tags[0].split(',')
        tag_objects = [Tag.objects.get_or_create(name=name)[0] for name in tags]
        print('Tag objects: ', tag_objects)
        
        ####
        content = request_copy['content'] 
        bs64_images = extract_base64_images(content)
        
        created_images = []
        
        if (bs64_images):
            for bs64_image in bs64_images:
                print("base64_images first 10: ", bs64_image[:10])
                print("base64_images last 10: ", bs64_image[-10:-1])
                image_data = ContentFile(base64.b64decode(bs64_image), name=f'{generate_random_name(12)}.jpeg')
                created_image = Image.objects.create(image = image_data)
                created_images.append(created_image)
                print('Created image: ', created_image)
                
                image_url = get_image_url(created_image)
                print('image url: ', image_url)
                content = replace_base64_with_urls(content, bs64_image, image_url)
            print('After replacing content with urls: ', content)
            
            request_copy['content'] = content
        
        print('request_copy: ', request_copy)
        
        serializer = self.get_serializer(data=request_copy, instance=instance, partial=True)
        print('serializer: ', serializer)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            serializer.instance.edited = datetime.now()    
            print(f'tag_objects: {tag_objects}')
            serializer.instance.tags.set(tag_objects)
            serializer.instance.save()
            
            for image in created_images:
                image.post = serializer.instance
                image.save()
                
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
