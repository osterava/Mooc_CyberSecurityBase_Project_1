from django.urls import path
from .views import home, LoginView, profile, create_post, blog_detail, delete_post, logout_view, search_blogs,register

urlpatterns = [
    path('', home, name='home'), 
    path('login/', LoginView.as_view(), name='login'),  
    path('profile/', profile, name='profile'), 
    path('create_post/', create_post, name='create_post'),  
    path('blogs/<int:post_id>/', blog_detail, name='blog_detail'),  
    path('delete/<int:post_id>/delete/', delete_post, name='delete_post'), 
    path('logout/', logout_view, name='logout'),
    path('search/', search_blogs, name='search_blogs'),
    path('registration/', register, name="registration")
]
