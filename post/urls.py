from django.urls import path
from .views import create_post, delete_post, detail_post, update_comment, update_post, delete_post, delete_comment, PostListView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user_posts'),
    path('detail/<int:pk>/', detail_post, name='detail_post'),
    
    path('create/', create_post, name='create_post'),
    path('update/<int:pk>/', update_post, name='update_post'),
    path('update_comment/<int:pk>/', update_comment, name='update_comment'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    
]
