from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include blog app URLs at the root, not just login
]