from rest_framework import serializers
from .models import Tag, Post, Comment, Profile

class TagSerializer(serializers.ModelSerializer): # это сериализатор для модели Tag, который преобразует объекты модели в формат JSON и обратно
    class Meta: # настройки сериализатора
        model = Tag #это модель, для которой создается сериализатор
        fields = ['id', 'name'] #это список полей модели, которые будут включены в сериализованный вывод. В данном случае это id и name
        
        
class PostSerializer(serializers.ModelSerializer): 
    author = serializers.CharField(
        source='author.username', # source='author.username' — взять имя связанного пользователя;
        read_only=True, # read_only=True — клиент может увидеть автора, но не может сам указать его имя.
    )
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'tags',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at'] # read_only_fields = ['created_at', 'updated_at'] — эти поля будут доступны только для чтения, клиент не сможет их изменять.
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True,
    )
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'content',
            'created_at',
        ]
        read_only_fields = ['created_at']
        

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source='user.username',
        read_only=True,
    )
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'bio',
            'avatar_url',
        ]