from django.urls import path
from .views import tag_list, tag_detail

urlpatterns = [
    path('tags/', tag_list, name='tag-list'),
    path('tags/<int:pk>/', tag_detail, name='tag-detail'),
]