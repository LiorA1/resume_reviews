
from django.urls import path
from .views import register, profile

app_name = "accounts"

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
