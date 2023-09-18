from .models import Posts, Threads, Tags, Comments, Likes, Dislikes
from rest_framework import serializers

class ThreadSerializer(serializers.ModelSerializer):
    pass

class PostSerializer(serializers.ModelSerializer):
    

    created_date = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Posts,
        fields = ('id', 'title', 
                  'content', 'author', 
                  'likes', 'dislikes', 'thread', 
                  'created_date', 'modified_date')

