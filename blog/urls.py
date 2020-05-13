from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post-home'),
    path('user/<str:username>/', views.AuthorPostListView.as_view(), name='author-posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    #path('author_posts/<int:id>/', views.author_post, name='author-posts'),
    
]