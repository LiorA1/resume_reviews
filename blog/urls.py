
from django.urls import path
from django.urls.base import reverse_lazy
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.blog_home, name="blog_home"),

    # Posts CRUD
    path('list/', views.PostListView.as_view(), name="post_list"),
    path('post/create/', views.PostCreateView.as_view(success_url=reverse_lazy(f'{app_name}:post_list')), name="post_create"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(success_url=reverse_lazy(f'{app_name}:post_list')), name="post_delete"),

    # Comments CRUD
    path('post/<int:pk>/create_comment/', views.CommentCreateView.as_view(success_url=reverse_lazy(f'{app_name}:post_list')), name="comment_create"),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name="comment_detail"),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name="comment_update"),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(success_url=reverse_lazy(f'{app_name}:post_list')), name="comment_delete"),
]