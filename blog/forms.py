from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# Post Form for creating/editing blog posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# Comment Form for creating/editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Removed 'status' field as it will default to 'active'

    def save(self, commit=True):
        comment = super().save(commit=False)
        # Set the default 'active' status for all new comments
        if not comment.status:
            comment.status = 'active'
        if commit:
            comment.save()
        return comment