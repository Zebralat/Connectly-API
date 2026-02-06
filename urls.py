from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list_create, name='user_list_create'),
    path('posts/', views.post_list_create, name='post_list_create'),
    path('comments/', views.comment_list_create, name='comment_list_create'),
]