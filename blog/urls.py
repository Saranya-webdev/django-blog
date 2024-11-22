from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL points to home
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),  # Post delete URL
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),  # Comment delete URL
    path('post/create/', views.post_create, name='post_create'),  # Post creation URL
    path('post/<int:post_id>/edit/', views.post_update, name='post_update'),  # Post edit URL
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'), 
     # Edit comment URL
    path('register/', views.RegisterView.as_view(), name='register'),  # Registration URL
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Login URL
    # Add any other URLs as necessary
    
]