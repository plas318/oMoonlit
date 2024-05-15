from rest_framework import serializers
from .models import Tag, Post, Image, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'post']
        
            


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    def create(self, validated_data):
        print(f'validated_data: {validated_data}')        
        post = Post.objects.create(**validated_data)
        return post
    
    def update(self, instance, validated_data):
        print('instance: ', instance)
        print('validated_data: ', validated_data)
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.category = validated_data.get('category')
        return instance

    def partial_update(self, instance, validated_data):
        print('instance: ', instance)
        print('validated_data: ', validated_data)
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        if 'category' in validated_data:
            instance.category = validated_data.get('category')
        instance.save()
        
        return instance
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'created', 'edited', 'tags', 'images', 'author']
        extra_kwargs={
            'id' : {'read_only': True },
            'created' : {'format': "%Y/%m/%d"},
            'edited' : {'format': "%Y/%m/%d"}
        }
        
    

    


        