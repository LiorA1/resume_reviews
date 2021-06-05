from django.core.exceptions import ValidationError
from accounts.forms import ProfileUpdateForm
from django.test import TestCase
from ..models import CustomUser, Profile
# Create your tests here.

from django.conf import settings
# TDD

class CustomUserTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user_a = CustomUser(username='la', email='la@test.com')
        self.user_a.is_staff = True
        self.user_a.set_password('pass')
        self.user_a.save()

        return super().setUp()


    def test_user_exists(self):
        user_count = CustomUser.objects.count()
        print("user_count:", user_count)

        self.assertEqual(user_count, 1) #! checking equality

    
    def test_customuser_str(self):
        self.assertEqual(str(self.user_a), self.user_a.username)
    

    def test_profile_str(self):
        self.assertEqual(str(self.user_a.profile), f'{ self.user_a.username } Profile')


    from ..forms import ProfileUpdateForm
    def test_forms_profileupdateform(self):
        #form_u_profile = ProfileUpdateForm()
        #form_u_profile.is_valid()
        #self.assertRaises(ValidationError, form_u_profile.clean) # clean
        pass



    def test_user_password(self):
        pass


    def test_customusers_profile(self):
        num_of_users = CustomUser.objects.count()
        num_of_profiles = Profile.objects.count()
        print(num_of_users, num_of_profiles)

        self.assertEqual(num_of_users, num_of_profiles)



class ProfileTestCase(TestCase):
    pass

