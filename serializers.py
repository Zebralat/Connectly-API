from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - includes role for RBAC"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model with privacy field"""
    
    author_username = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.IntegerField(source='liked_by.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'content', 
            'author', 
            'author_username',
            'privacy',          
            'like_count',
            'comment_count',
            'created_at'
        ]
        read_only_fields = ['author', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id', 
            'post', 
            'author', 
            'author_username',
            'content', 
            'created_at'
        ]
        read_only_fields = ['author', 'created_at']