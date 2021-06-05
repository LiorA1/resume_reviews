
from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()

router.register(r'reviews', views.ReviewViewSet)
router.register(r'resumes', views.ResumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]