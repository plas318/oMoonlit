from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return f'Category: {self.name}'
    
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Tag: {self.name}'
    
    
class Post(models.Model):
    '''
    Post / Article Supports RTE (Rich Text Editor)
    '''
    title = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_created=True, auto_now_add= True)
    edited = models.DateTimeField(auto_created=True, auto_now= True)
    content = models.TextField(max_length=4000)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    tags = models.ManyToManyField(Tag, blank=True)
        
    def __str__(self):
        return f'Post: {self.title} : pk({self.author.get_username()}), created-date: {self.created}, category: {self.category}\
                 tags: {self.tags}' 
    
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to='posted_images/')
    
    def __str__(self) -> str:
        return f'Image: {self.image.name}'
    

# class Comment(models.Model):
#     '''
#     Postpone Until there is a solution for guest posting, etc..
#     '''
#     # author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
#     user = models.CharField(max_length=30, null=False)
#     pw = models.CharField(max_length=30)
#     # If the comment is replying to some other comment, refer the other comment
#     parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="reply")
#     created = models.DateTimeField(auto_created=True, auto_now_add= True)
#     edited = models.DateTimeField(auto_created=True, auto_now= True)
#     content = models.TextField(max_length=1000)
    
    
#     def __str__(self):
#         return f'Comment: "post:{self.post.title}" {self.content}'
    
