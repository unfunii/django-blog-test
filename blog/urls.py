from django.urls import path, include
from .views import TagViewSet, PostViewSet, CommentViewSet, ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter() # DefaultRouter() — это класс, который автоматически создает маршруты для стандартных действий (list, create, retrieve, update, destroy) для модели Post.

router.register('tags', TagViewSet, basename='tag')
router.register('posts', PostViewSet, basename='post') 
router.register('comments', CommentViewSet, basename='comment') 
router.register('profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    # path('tags/', tag_list, name='tag-list'),
    # path('tags/<int:pk>/', tag_detail, name='tag-detail'),
    path('', include(router.urls)),
]