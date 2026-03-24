from django.urls import path
from .views import (
    toggle_like,
    create_comment,
    list_comments,
    user_list_create,
    post_list_create,
    post_detail,        
    delete_post,        
    GoogleLogin,
    feed,
)

urlpatterns = [
    path('', post_list_create, name='post-list-create'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('<int:pk>/delete/', delete_post, name='delete-post'),
    path('<int:pk>/like/', toggle_like, name='toggle-like'),
    path('<int:pk>/comment/', create_comment, name='create-comment'),
    path('<int:pk>/comments/', list_comments, name='list-comments'),
    path('users/', user_list_create, name='user-list-create'),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('feed/', feed, name='feed'),
]