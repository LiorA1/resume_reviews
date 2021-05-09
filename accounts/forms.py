from django import forms
from django.core.files.images import get_image_dimensions
from .models import Profile

#from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

# The Creation of a Profile is automatic, so need only to make a form for update (and only image for now)

# WE extend the creationform, because of the email
"""User Register Form"""

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CustomUserRegisterForm(CustomUserCreationForm):
    email = forms.EmailField()  # Required ?

    # Configuration
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']



'''Create a UserUpdateForm to update username and email'''
class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


from django.core.files.images import get_image_dimensions

class ProfileUpdateForm(forms.ModelForm):
    """Create a ProfileUpdateForm to update image"""

    class Meta:
        model = Profile
        fields = ['image']

    def clean_image(self):
        # super().clean_image()
        image = self.cleaned_data['image']

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
            if len(image) > (20 * 1024):
                raise forms.ValidationError(
                    f'Image file size may not exceed 20k.')

        except AttributeError as e:
            """
            Handles case when we are updating the user profile and dont supply an image
            """
            #self.add_error("image", e)
            pass

        return image


# https://github.com/django/django/blob/main/django/forms/forms.py#L361

# https://stackoverflow.com/questions/38523456/how-to-put-in-a-profile-picture-in-django


# https://www.devhandbook.com/django/class-based-views/
