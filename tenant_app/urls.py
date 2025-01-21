from django.urls import path
from .views import blog_list, create_blog_post, blog_detail, register, user_login, notifications,user_logout,search_blog_posts

urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/create/', create_blog_post, name='create_blog_post'),
    path('blogs/<int:post_id>/', blog_detail, name='blog_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('search/', search_blog_posts, name='search_blog_posts'),
    path('notifications/', notifications, name='notifications'),

]