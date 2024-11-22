from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

# Application imports
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .forms import PostForm, CommentForm

# Home view with pagination
def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

# Post detail view with comments and comment form
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')
        
        if comment_id:
            # Edit existing comment
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.author == request.user:
                comment.content = content
                comment.save()
                return redirect('post_detail', post_id=post.id)
        else:
            # Add new comment
            if content:
                Comment.objects.create(post=post, author=request.user, content=content, status='active')
                return redirect('post_detail', post_id=post.id)

    comments = post.comments.filter(status='active')  # Show only active comments
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

# Create a new post, only accessible to authenticated users
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(title=title, content=content, author=request.user)
            return redirect('home')
    return render(request, 'post_create.html')

# Update a post
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'post_update.html', {'post': post})

# Delete a post
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('home')
    return redirect('post_detail', post_id=post.id)

# Delete a comment
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()  # Consider soft deletion if required
        return redirect('post_detail', post_id=post_id)
    return redirect('post_detail', post_id=post_id)

# Edit a comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})

# Registration view
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists. Please choose a different one."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User registered successfully!'}, status=201)

# Login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Pagination for posts
class PostPagination(PageNumberPagination):
    page_size = 10

# Post viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['title']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required"}, status=400)
        comment = Comment.objects.create(post=post, author=request.user, content=content, status='active')
        return Response(CommentSerializer(comment).data)

# Comment viewset
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.request.data['post'])
        except Post.DoesNotExist:
            return Response({"error": "Invalid post ID"}, status=400)
        serializer.save(author=self.request.user, post=post, status='active')