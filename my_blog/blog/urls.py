from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', blog, name='blog'),
    path('posts', post_list, name='post_list'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
]