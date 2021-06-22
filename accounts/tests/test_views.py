
from accounts.models import CustomUser
from django.core.handlers.wsgi import WSGIRequest
from accounts.views import profile
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls import reverse
import os.path

# AssertIs Versus AssertEqual:
# https://stackoverflow.com/q/7281774/3790620


class AccountsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        FOLDER_NAME = 'data'
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        cls.TEST_DATA_DIR = os.path.join(TEST_DIR, FOLDER_NAME)

        return super().setUpTestData()


    def setUp(self) -> None:
        self.login_url = reverse('login')
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }

        self.client = Client()
        self.user = get_user_model().objects.create_user(**self.data_of_user)
        
        return super().setUp()


class RegisterViewTest(AccountsViewsTests):
    '''Test register/login views'''
    # https://stackoverflow.com/q/55351366/3790620
    # https://stackoverflow.com/q/5660952/3790620


    def setUp(self) -> None:
        self.registration_url = reverse('accounts:register')
        self.data_of_user_registration = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'dsfdsf4543543hgjh',
            'password2': 'dsfdsf4543543hgjh',
        }
        return super().setUp()


    def test_signup_page_url_and_name(self):
        response_of_registration = self.client.get(self.registration_url)
        self.assertEqual(response_of_registration.status_code, 200)
        self.assertTemplateUsed(response_of_registration, template_name='accounts/register.html')


    '''tests the register process'''
    def test_register_action_with_existing_user(self):
        """ Test the register action, with an existing user"""

        self.assertEqual(CustomUser.objects.count(), 1)
        # register a user
        response_of_post = self.client.post(
            self.registration_url, 
            data=self.data_of_user_registration, 
            follow=True)

        self.assertEqual(response_of_post.context['form'].errors['username'], ['A user with that username already exists.'])
        self.assertEqual(response_of_post.status_code, 200)
        self.assertTemplateUsed(response_of_post, template_name='accounts/register.html') #used when the user exists allready


    '''tests the register process'''
    def test_register_action_with_default_image(self):
        """ Test the register action, with a new user"""

        self.data_of_user_b_registration = {
            'username': 'testb',
            'email': 'test@test.com',
            'password1': 'why8eightgfD',
            'password2': 'why8eightgfD',
        }

        self.assertEqual(CustomUser.objects.count(), 1)

        # register a user
        response_of_post = self.client.post(
            self.registration_url, 
            data=self.data_of_user_b_registration, 
            follow=True)

        self.assertEqual(CustomUser.objects.count(), 2)
        
        user_pk = 2
        # get the user
        user = get_user_model().objects.get(username=self.data_of_user_b_registration['username'])
        

        # checks that the user is indeed inside the DB.
        self.assertEqual(response_of_post.status_code, 200)
        self.assertEqual(self.data_of_user_b_registration['username'], str(user))
        self.assertTemplateUsed(response_of_post, template_name='registration/login.html') #used when the user is new

        #! AWS Cleanup 
        #CustomUser.objects.get(username=self.user.username).delete()
        #! Not needed here, because it Uses the default image





from django.conf import settings

class LoginViewTest(AccountsViewsTests):

    
    def setUp(self) -> None:

        return super().setUp()


    def test_login_url(self):
        """Test the existness of the login url"""
        self.assertEqual(f'{settings.LOGIN_URL}', self.login_url)


    def test_login_logout(self):
        """Test the login logout process"""
        #login
        response_of_login = self.client.login(**self.data_of_user)
        self.assertTrue(response_of_login)

        #get to the login page again
        response_of_get = self.client.get(self.login_url)
        self.assertEqual(response_of_get.status_code, 200)

        # Go to some directory
        resumes_home_url = reverse('resumes:home')
        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        #print(response_of_get.content)
        #?self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')

        ## Check that the user that we login with, is the one that django auth. 
        # https://gist.github.com/bengolder/c9dc7006f9d6b4d17d5af5465115df73
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user, self.user)
        self.assertTrue(client_user.is_authenticated)
        # In the MDN this is done differently.
        # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


        #Log Out
        self.client.logout()

        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        client_user = auth.get_user(self.client)
        self.assertNotEqual(client_user, self.user)
        self.assertFalse(client_user.is_authenticated)


class ProfileViewTest(AccountsViewsTests):

    def setUp(self) -> None:
        self.profile_url = reverse('accounts:profile')
        FOLDER_NAME = 'data'
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TEST_DATA_DIR = os.path.join(TEST_DIR, FOLDER_NAME)
        return super().setUp()


    def build_update_profile_request(self, username: str, email: str, image_path: str, image_name: str) -> WSGIRequest:
        """ helper method: build an update profile WSGI request"""

        from django.core.files.uploadedfile import SimpleUploadedFile
        #POST request to the profile page 
        u_form_data = {
            "username": username,
            "email": email
        }
        p_form_data = {

        }
        

        # build a request
        with open(image_path, 'rb') as fhandler:
            p_form_data['image'] = SimpleUploadedFile(
                name=image_name, 
                content=fhandler.read(), 
                content_type="image/png")
            
            u_form_data.update(p_form_data)
            #url_post_profile = reverse(self.profile_url)
            update_profile_request = RequestFactory().post(
                self.profile_url, 
                data=u_form_data)
            update_profile_request.user = self.user

        return update_profile_request

    def proccess_request_middleware(self, request: WSGIRequest) -> WSGIRequest:
        """ helper method: add messages and session data to an WSGI request"""
        from django.contrib.sessions.middleware import SessionMiddleware
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request)
        request.session.save()

        from django.contrib.messages.middleware import MessageMiddleware
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request)
        request.session.save()

        return request


    def test_profile_view_get(self):
        """Test the get-redirect path for anonymous user"""
        #GET request to the profile page 
        response_of_get = self.client.get(self.profile_url)
        self.assertEqual(response_of_get.status_code, 302)
        #self.assertTemplateUsed(response_of_get, template_name='accounts/profile.html')
        self.assertRedirects(response_of_get, response_of_get.url, 302, 200)

        #GET request to the profile page 
        response_of_get = self.client.get(response_of_get.url)
        self.assertEqual(response_of_get.status_code, 200)
        self.assertTemplateUsed(response_of_get, template_name='registration/login.html')
        
  
    def test_profile_get_after_login(self):
        """Test the profile view for authorized user"""
        #login
        response_of_login = self.client.login(**self.data_of_user)
        self.assertTrue(response_of_login)

        #GET request to the profile page 
        response_of_get = self.client.get(self.profile_url)
        self.assertEqual(response_of_get.status_code, 200)
        self.assertTemplateUsed(response_of_get, template_name='accounts/profile.html')


    def test_profile_view_invalid_user_data(self):
        """Test the profile view for invalid data"""

        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.get(username=self.data_of_user['username'])
        self.assertEqual(str(user), self.data_of_user['username'])

        #login
        response_of_login = self.client.login(**self.data_of_user)
        self.assertTrue(response_of_login)

        
        #post request to the profile page without any data
        response_of_post = self.client.post(self.profile_url)
        self.assertEqual(response_of_post.status_code, 200)
        self.assertTemplateUsed(response_of_post, template_name='accounts/profile.html')

        ## Check errors existness
        #print("Testing:u_form errors:", response_of_post.context['u_form'].errors['email'])
        #print("Testing:p_form errors:", response_of_post.context['p_form'].errors)
        self.assertEqual(response_of_post.context['u_form'].errors['username'], ['This field is required.'])
        self.assertEqual(response_of_post.context['u_form'].errors['email'], ['This field is required.'])
        #self.assertEqual(response_of_post.context['p_form'].errors['image'], ['Please use an image that is 300 x 300 pixels or less'])

        ## Check messages existness
        self.assertTrue(response_of_post.context['messages'].added_new)
        #print(response_of_post.context['messages'].__dict__)
        #if response_of_post.context['messages']:
        #    for message in response_of_post.context['messages']:
        #        print("Testing:Messages:", message.message.items())


        # Go to some directory
        resumes_home_url = reverse('resumes:home')
        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        #?self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')


        #Log Out
        self.client.logout()

        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        client_user = auth.get_user(self.client)
        self.assertNotEqual(client_user, self.user)
        self.assertFalse(client_user.is_authenticated)

        #! AWS Cleanup
        #print(CustomUser.objects.count())
        #CustomUser.objects.get(username=self.user.username).delete()
        #! No image was supplied
        


    def test_profile_view_valid(self):
        """Test the profile view with valid data"""
        #login
        response_of_login = self.client.login(**self.data_of_user)
        self.assertTrue(response_of_login)

        # Now, correctly
        u_form_data = {
            "username": self.data_of_user['username'],
            "email": self.data_of_user["email"]
        }

        ## Create a request
        FILE_NAME = 'small.png'
        image_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        ## Build a request
        request_profile = self.build_update_profile_request(
            u_form_data['username'], 
            u_form_data['email'], 
            image_file_path, FILE_NAME)
        

        # proccess the request with middleware
        request_profile = self.proccess_request_middleware(request_profile)
        

        # Make a request
        response_of_post = profile(request_profile)

        ## Checks
        self.assertEqual(response_of_post.status_code, 302)

        ## Check redirect url
        self.assertEqual(response_of_post.url, self.profile_url)

        ## Check 200 Code after the redirect 
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        self.assertFalse(response_of_redirect.context['messages'].added_new)
        
        ## Check profile for messages
        #if response_of_redirect.context['messages']:
        #    for message in response_of_redirect.context['messages']:
        #        print("Testing:Messages:", message)

        

        # Go to some directory
        resumes_home_url = reverse('resumes:home')
        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        #?self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')


        #Log Out
        self.client.logout()

        response_of_get = self.client.get(resumes_home_url)
        self.assertEqual(response_of_get.status_code, 200)
        client_user = auth.get_user(self.client)
        self.assertNotEqual(client_user, self.user)
        self.assertFalse(client_user.is_authenticated)

        #! AWS Cleanup
        #print(CustomUser.objects.count())
        CustomUser.objects.get(username=self.user.username).delete()

    