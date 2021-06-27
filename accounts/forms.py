from django import forms
from django.core.files.images import get_image_dimensions
from .models import Profile

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

from django.core.files.images import get_image_dimensions


class CustomUserCreationForm(UserCreationForm):
    """CustomUser Creation Form"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


# we extend the creationform, because of the email
class CustomUserRegisterForm(CustomUserCreationForm):
    """CustomUser Register Form"""
    email = forms.EmailField()

    # Configuration
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserUpdateForm(forms.ModelForm):
    '''CustomUserUpdateForm to update username and email'''
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Create a ProfileUpdateForm to update image"""

    class Meta:
        model = Profile
        fields = ['image']

    def clean_image(self):
        # super().clean_image()
        image = self.cleaned_data['image']
        # print("ProfileUpdateForm:clean_image")

        try:
            w, h = get_image_dimensions(image)

            # Validate dimensions
            max_width = max_height = 300
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Please use an image that is {max_width} x {max_height} pixels or less')

            # Validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
                raise forms.ValidationError(
                    f'Please use a jpeg, jpg, gif, png images only')

            # Validate file size
            image_size = len(image)  # return the bytes size.
            limit_kbyte = 200
            limit_size = (limit_kbyte * 1024)
            if image_size > limit_size:
                raise forms.ValidationError(f'Your Image is {image_size}. Image file size may not exceed {limit_kbyte}k.')

        except AttributeError as e:
            """
            Handles case:
            when we are updating the user profile and dont supply an image
            """
            # self.add_error("image", e)
            pass

        return image


# https://github.com/django/django/blob/main/django/forms/forms.py#L361

# https://stackoverflow.com/questions/38523456/how-to-put-in-a-profile-picture-in-django


# https://www.devhandbook.com/django/class-based-views/
