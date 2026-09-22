# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions

from .models import Tag, Post, Comment, Profile
from .serializers import TagSerializer, PostSerializer, CommentSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly, IsProfileOwnerOrReadOnly

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.

# @api_view(['GET', 'POST'])
# def tag_list(request):
#     if request.method == 'GET':
#         tags = Tag.objects.all() # это запрос к базе данных, который получает все объекты модели Tag. Метод all() возвращает QuerySet, содержащий все записи в таблице Tag.
#         serializer = TagSerializer(tags, many=True) 
#         return Response(serializer.data)
    
#     elif request.method == 'POST': # request.method — способ запроса: GET, POST, PATCH;
#         serializer = TagSerializer(data=request.data) # request.data — данные, отправленные пользователем;
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
        
#         return Response(serializer.errors, status=400)

# Model получает информацию из базы;
# Serializer преобразует и проверяет информацию;
# View решает, что сделать при запросе;
# URL приводит запрос к нужному View.

# @api_view(['GET', 'PATCH', 'DELETE'])
# def tag_detail(request, pk): #pk = primary key(ex. id), первичный ключ, уникальный идентификатор записи в базе данных. В данном случае pk используется для получения конкретного объекта модели Tag по его идентификатору.
#     tag = get_object_or_404(Tag, pk=pk) # get_object_or_404 — это функция, которая получает объект модели Tag по первичному ключу pk. Если объект не найден, возвращается ошибка 404.
    
#     if request.method == 'GET':
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)
    
#     elif request.method == 'PATCH':
#         serializer = TagSerializer(
#             tag, # какой объект изменить
#             data=request.data, # какие новые данные записать
#             partial=True # partial=True означает, что при обновлении объекта можно передавать только часть полей, а не все поля модели. Это позволяет обновлять только те поля, которые были изменены пользователем, без необходимости отправлять все данные объекта.
#         )
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=400)
    
#     elif request.method == 'DELETE':
#         tag.delete()
#         return Response(status=204) # 204 No Content — это статус-код HTTP, который указывает на успешное выполнение запроса, но без возвращаемого содержимого. В данном случае он используется для подтверждения успешного удаления объекта Tag из базы данных.

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # permissions.IsAuthenticatedOrReadOnly — это класс, который определяет права доступа к представлению. Он позволяет аутентифицированным пользователям выполнять любые действия (создание, обновление, удаление), а неаутентифицированным пользователям разрешает только чтение данных (GET-запросы).


class PostViewSet(viewsets.ModelViewSet): # viewsets.ModelViewSet — это класс, который предоставляет набор стандартных действий для работы с моделью Post. Он автоматически создает методы для обработки запросов GET, POST, PUT, PATCH и DELETE.
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly,
    ] # permissions.IsAuthenticatedOrReadOnly — это класс, который определяет права доступа к представлению. Он позволяет аутентифицированным пользователям выполнять любые действия (создание, обновление, удаление), а неаутентифицированным пользователям разрешает только чтение данных (GET-запросы).
    
    
    def perform_create(self, serializer): # perform_create — это метод, который вызывается при создании нового объекта модели Post. Он позволяет настроить процесс сохранения объекта перед его сохранением в базе данных.
        serializer.save(author=self.request.user) # self.request.user — это текущий аутентифицированный пользователь, который отправил запрос. Метод save() сохраняет новый объект Post в базе данных, устанавливая автора как текущего пользователя.
        
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comments',
            {
                'type': 'new_comment',
                'data': CommentSerializer(comment).data,
            }
        )
    

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProfileOwnerOrReadOnly,
    ]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)