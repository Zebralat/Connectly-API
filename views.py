from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .singleton import LoggerSingleton
from .factory import PostFactory

# Initialize Singleton Logger
logger = LoggerSingleton()

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) # Anyone can see or create a user
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        # --- SECURITY: Hashing Password ---
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.log(f"User {data.get('username')} created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # Must be logged in to see/create posts
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        # --- DESIGN PATTERN: Factory Pattern ---
        try:
            post = PostFactory.create_post(
                author_id=request.data.get('author'),
                content=request.data.get('content')
            )
            serializer = PostSerializer(post)
            logger.log(f"Post created by User ID {request.data.get('author')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.log(f"Comment added to post {request.data.get('post')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)