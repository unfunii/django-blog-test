from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer

from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(['GET', 'POST'])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all() # это запрос к базе данных, который получает все объекты модели Tag. Метод all() возвращает QuerySet, содержащий все записи в таблице Tag.
        serializer = TagSerializer(tags, many=True) 
        return Response(serializer.data)
    
    elif request.method == 'POST': # request.method — способ запроса: GET, POST, PATCH;
        serializer = TagSerializer(data=request.data) # request.data — данные, отправленные пользователем;
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

# Model получает информацию из базы;
# Serializer преобразует и проверяет информацию;
# View решает, что сделать при запросе;
# URL приводит запрос к нужному View.

@api_view(['GET', 'PATCH', 'DELETE'])
def tag_detail(request, pk): #pk = primary key(ex. id), первичный ключ, уникальный идентификатор записи в базе данных. В данном случае pk используется для получения конкретного объекта модели Tag по его идентификатору.
    tag = get_object_or_404(Tag, pk=pk) # get_object_or_404 — это функция, которая получает объект модели Tag по первичному ключу pk. Если объект не найден, возвращается ошибка 404.
    
    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TagSerializer(
            tag, # какой объект изменить
            data=request.data, # какие новые данные записать
            partial=True # partial=True означает, что при обновлении объекта можно передавать только часть полей, а не все поля модели. Это позволяет обновлять только те поля, которые были изменены пользователем, без необходимости отправлять все данные объекта.
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=204) # 204 No Content — это статус-код HTTP, который указывает на успешное выполнение запроса, но без возвращаемого содержимого. В данном случае он используется для подтверждения успешного удаления объекта Tag из базы данных.