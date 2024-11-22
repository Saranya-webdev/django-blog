from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Nested serialization for read-only
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Validate post relation

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # Mark these as read-only


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Nested serialization for read-only
    comments = CommentSerializer(many=True, read_only=True)  # Include related comments as read-only

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['created_at', 'updated_at']  # Mark these as read-only