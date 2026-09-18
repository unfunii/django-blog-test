from django.db import models
from django.conf import settings

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile',
    )
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey( #один автор может написать много постов, но каждый пост принадлежит только одному автору
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    tags = models.ManyToManyField( #один пост может иметь много тегов, и один тег может принадлежать многим постам
        Tag,
        related_name='posts',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey( #один пост может иметь много комментариев, но каждый комментарий принадлежит только одному посту
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey( #один автор может написать много комментариев, но каждый комментарий принадлежит только одному автору
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:50]