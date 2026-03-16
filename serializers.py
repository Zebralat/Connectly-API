from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User as CustomUser, Post, Comment  # if you have custom User, use that

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # or User
        fields = ['id', 'username', 'email', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)            
    like_count = serializers.ReadOnlyField(source='liked_by.count')
    comment_count = serializers.ReadOnlyField(source='comments.count')

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'like_count', 'comment_count']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    content = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at', 'post']