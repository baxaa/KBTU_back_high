from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Add tags if required


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # Use CustomUser instead of User
        fields = ['username', 'email', 'password', 'bio']  # Include the bio field


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']