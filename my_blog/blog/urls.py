from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', blog, name='blog'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),  # Post editing view
    path('posts/<int:post_id>/delete/', post_delete, name='post_delete'),  # Post deleting
    path('register/', register, name='register'),  # Registration
    path('login/', user_login, name='login'),  # Login
    path('logout/', user_logout, name='logout'),  # Logout



]