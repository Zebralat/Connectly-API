from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q  

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .singleton import LoggerSingleton

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

logger = LoggerSingleton()


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_list_create(request):
    """Handle GET (list all users) and POST (create new user)"""
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
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
@permission_classes([IsAuthenticated])
@csrf_exempt
def post_list_create(request):
    """List all posts (GET) or create a new post (POST).
    New posts default to 'public' unless 'private' is specified."""
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            post = Post.objects.create(
                author=request.user,
                content=request.data.get('content'),
                privacy=request.data.get('privacy', 'public')   
            )
            serializer = PostSerializer(post)
            logger.log(f"Post created by User {request.user.username} with privacy {post.privacy}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    """Get single post - enforces privacy settings.
    Only the post owner can view their private posts."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if post.privacy == 'private' and post.author != request.user:
        return Response({"error": "This post is private"}, status=status.HTTP_403_FORBIDDEN)

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_post(request, pk):
    """Only users with role='admin' can delete any post (Role-Based Access Control)"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 'admin':
        return Response({"error": "Only admins can delete posts"}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    logger.log(f"Admin {request.user.username} deleted post {pk}")
    return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_comment(request, pk):
    """Only admins can delete any comment (Role-Based Access Control)"""
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 'admin':
        return Response({"error": "Only admins can delete comments"}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    logger.log(f"Admin {request.user.username} deleted comment {pk}")
    return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def toggle_like(request, pk):
    """Toggle like on a post: add if not liked, remove if already liked."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user in post.liked_by.all():
        post.liked_by.remove(user)
        action = "unliked"
    else:
        post.liked_by.add(user)
        action = "liked"

    logger.log(f"User {user.username} {action} post {pk}")

    return Response({
        "status": action,
        "like_count": post.liked_by.count()
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_comment(request, pk):
    """Create a new comment on a specific post.
    Author is automatically set to the logged-in user."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content')
    if not content or not content.strip():
        return Response({"content": ["This field is required and cannot be blank."]}, 
                        status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content.strip()
    )

    logger.log(f"Comment added to post {pk} by {request.user.username}")

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments(request, pk):
    """Return all comments for a specific post, ordered by newest first."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    comments = post.comments.all().order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    """Google OAuth2 login endpoint using allauth and dj-rest-auth"""
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    """News feed with pagination and privacy enforcement.
    Users see: all public posts + their own private posts."""
    posts = Post.objects.filter(
        Q(privacy='public') | Q(author=request.user)
    ).order_by('-created_at')

    page = int(request.query_params.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size

    paginated_posts = posts[start:end]

    serializer = PostSerializer(paginated_posts, many=True)
    return Response({
        "results": serializer.data,
        "count": posts.count(),
        "page": page,
        "pages": (posts.count() + page_size - 1) // page_size
    })