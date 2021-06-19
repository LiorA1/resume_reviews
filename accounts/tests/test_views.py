from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
 
# AssertIs Versus AssertEqual:
# https://stackoverflow.com/q/7281774/3790620


class RegisterViewTest(TestCase):
    '''Test register/login views'''
    # https://stackoverflow.com/q/55351366/3790620
    # https://stackoverflow.com/q/5660952/3790620


    #def setUp(self) -> None:
    #    self.username = "testuser"
    #    self.email = "test@me.ai"
    #    self.password = "passgfkrf5s3f8"
    #    return super().setUp()

    #@classmethod
    #def setUpTestData(cls) -> None:
    #    # One creation of data(Versus setUp)
    #    return super().setUpTestData()


    def test_signup_page_url_and_name(self):
        url = reverse('accounts:register')
        #print(url)
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, template_name='accounts/register.html')


    '''tests the register process'''
    def test_register_action(self):
        url = reverse('accounts:register')
        #print("test_register_action:", url)
        data_of_user = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'dsfdsf4543543hgjh',
            'password2': 'dsfdsf4543543hgjh',
        }

        # register a user
        response_of_post = self.client.post(
            url,
            data=data_of_user,
            follow=True
        )
        #print(response_of_post.content)

        # get all users
        users = get_user_model().objects.all()
        #print("users:", users)

        # checks that the user is indeed inside the DB.
        self.assertEqual(response_of_post.status_code, 200)
        self.assertEqual(data_of_user['username'], str(users.first()))
        self.assertTemplateUsed(response_of_post, template_name='registration/login.html')





from django.conf import settings

class LoginViewTest(TestCase):

    
    def setUp(self) -> None:
        self.url = reverse('login')
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
        }
        self.client = Client()

        self.user = get_user_model().objects.create_user(**self.data_of_user)
        # Create a User
        #print("Num:", get_user_model().objects.count())

        return super().setUp()


    def test_login_url(self):
        #login_url = "/login/"
        #print(f'/accounts{settings.LOGIN_URL}')
        self.assertEqual(f'/accounts{settings.LOGIN_URL}', self.url)


    def test_login_logout(self):
        #login
        response_of_login = self.client.login(**self.data_of_user)
        #print(response_of_login)
        self.assertTrue(response_of_login)

        #get to the login page again
        response_of_get = self.client.get(reverse('login'))
        self.assertEqual(response_of_get.status_code, 200)

        # Go to some directory
        url = reverse('resumes:home')
        #print(url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)
        #?self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')

        # https://gist.github.com/bengolder/c9dc7006f9d6b4d17d5af5465115df73
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user, self.user)
        self.assertTrue(client_user.is_authenticated)
        #print("======")
        #print(hasattr(response_of_get.context, 'user'))
        #print(response_of_get.context['user'])
        #print("======")
        # In the MDN this is done differently.
        # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


        #Log Out
        self.client.logout()

        response_of_get = self.client.get(reverse('resumes:home'))
        self.assertEqual(response_of_get.status_code, 200)
        client_user = auth.get_user(self.client)
        self.assertNotEqual(client_user, self.user)
        self.assertFalse(client_user.is_authenticated)


class ProfileViewTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('login')
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
        }
        self.client = Client()

        self.user = get_user_model().objects.create_user(**self.data_of_user)
        # Create a User
        #print("Num:", get_user_model().objects.count())

        return super().setUp()


    def test_profile_view(self):
        #login
        response_of_login = self.client.login(**self.data_of_user)
        #print(response_of_login)
        self.assertTrue(response_of_login)

        #get request to the profile page 
        response_of_get = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response_of_get.status_code, 200)
        self.assertTemplateUsed(response_of_get, template_name='accounts/profile.html')

        #post request to the profile page 
        response_of_post = self.client.post(reverse('accounts:profile'))
        self.assertEqual(response_of_post.status_code, 200)
        
        
        #print("Testing:u_form errors:", response_of_post.context['u_form'].errors['email'])
        #print("Testing:p_form errors:", response_of_post.context['p_form'].errors['image'])
        self.assertEqual(response_of_post.context['u_form'].errors['username'], ['This field is required.'])
        self.assertEqual(response_of_post.context['u_form'].errors['email'], ['This field is required.'])
        self.assertEqual(response_of_post.context['p_form'].errors['image'], ['Please use an image that is 300 x 300 pixels or less'])
        

        # Go to some directory
        url = reverse('resumes:home')
        #print(url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)
        #?self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')


        #Log Out
        self.client.logout()

        response_of_get = self.client.get(reverse('resumes:home'))
        self.assertEqual(response_of_get.status_code, 200)
        client_user = auth.get_user(self.client)
        self.assertNotEqual(client_user, self.user)
        self.assertFalse(client_user.is_authenticated)

    