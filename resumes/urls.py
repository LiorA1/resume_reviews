"""resume_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy

from . import views

app_name="resumes"
urlpatterns = [
    #path('admin/', admin.site.urls),
    

    path('', views.home, name="home"),

    path('resume/list', views.ResumeListView.as_view(), name="resume_list"),
    path('user/resumes/<str:username>/', views.UserResumeListView.as_view(), name="user_resumes"),
    path('resume/create/', views.ResumeCreateView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="resume_create"),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name="resume_detail"),
    path('resume/<int:pk>/update/', views.ResumeUpdateView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="resume_update"),
    path('resume/<int:pk>/delete/', views.ResumeDeleteView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="resume_delete"),

    # Reviews CRUD (#TODO: Reviews list need to be according user)
    path('review/list', views.ReviewListView.as_view(), name="review_list"),
    path('user/reviews/<str:username>/', views.UserReviewListView.as_view(), name="user_reviews"),
    #path('review/create/', views.ReviewCreateView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="review_create"),
    path('resume/<int:pk>/create_review/', views.ReviewCreateView.as_view(), name="review_create"),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name="review_detail"),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="review_update"),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(success_url=reverse_lazy(f'{app_name}:home')), name="review_delete"),
]
