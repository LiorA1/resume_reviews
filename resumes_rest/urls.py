
from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views
router = DefaultRouter()

router.register(r'reviews', views.ReviewViewSet)
router.register(r'resumes', views.ResumeViewSet)

app_name = "resumes_rest"
urlpatterns = [
    path('', include(router.urls)),
]
