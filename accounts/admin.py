from django.contrib import admin
from .models import Profile
# Register your models here.

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser

from django.contrib.auth.admin import UserAdmin


admin.site.register(Profile)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserUpdateForm
    model = CustomUser
    list_display = ['email', 'username']
    # list_filter = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)


# TODO: 'Django Admin interface'
