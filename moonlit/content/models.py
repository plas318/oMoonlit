from django.db import models
from user.models import User

#Length Set
MAX_LENGTH_S = 30
MAX_LENGTH_M = 50
MAX_LENGTH_L = 2000

class Threads(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_S)
    description = models.CharField(max_length=MAX_LENGTH_M, blank=True)
    def __str__(self) -> str:
        return f"{self.name} {self.name}"

class Posts(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_S)
    content = models.TextField(max_length=2000)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=False)
    thread = models.ForeignKey(Threads, on_delete=models.SET_NULL)

    # Note on auto_created = True
    # auto_created => cannot be modified afterwards
    # auto_now => default input as current datetime(now)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.title}"

class Tags(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_S, unique=True)
    description = models.CharField(max_length=MAX_LENGTH_M, blank=True)
    def __str__(self) -> str:
        return f"{self.name} {self.description}"

class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"user: {self.author.alias} post: {self.post.title}\
                 likes: {self.is_liked} dislike: {self.is_disliked}"


class Comments(models.Model):
    content = models.CharField(max_length=MAX_LENGTH_L, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    replied = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.author.alias} {self.post.title} {self.created_at}"

class Notification(models.Model):
    content = models.CharField(max_length=MAX_LENGTH_L, blank=False)

    def __str__(self) -> str:
        return f""