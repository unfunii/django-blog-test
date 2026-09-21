from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer): # это сериализатор для модели Tag, который преобразует объекты модели в формат JSON и обратно
    class Meta: # это метакласс, который определяет поведение сериализатора
        model = Tag #это модель, для которой создается сериализатор
        fields = ['id', 'name'] #это список полей модели, которые будут включены в сериализованный вывод. В данном случае это id и name