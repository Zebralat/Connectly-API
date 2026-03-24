from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User with role for RBAC"""
    ROLE_CHOICES = [('admin', 'Admin'), ('user', 'User')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Post(models.Model):
    """Post with privacy setting"""
    PRIVACY_CHOICES = [('public', 'Public'), ('private', 'Private')]
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField('User', related_name='liked_posts', blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')

    def __str__(self):
        return f"Post by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"