from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Post

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return Response(data)

@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if username and email:
        User.objects.create(username=username, email=email)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    data = [{"id": p.id, "content": p.content, "author": p.author.id} for p in posts]
    return Response(data)

@api_view(['POST'])
def create_post(request):
    content = request.data.get('content')
    author_id = request.data.get('author') 
    try:
        author = User.objects.get(id=author_id)
        Post.objects.create(content=content, author=author)
        return Response({"message": "Post created successfully"}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)