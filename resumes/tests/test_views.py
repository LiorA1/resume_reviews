from resumes.forms import ResumeForm
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..views import ResumeCreateView, ResumeCreateView, ResumeDetailView
from ..models import Resume

from unittest import mock
from django.core.files import File

# Objectives:
# 0. Test home view
# 1. Test OwnerCreateView
# 2. Test ResumeUpdateView
# 3. Test ResumeDeleteView

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#views


class ResumeViews(TestCase):
    def setUp(self) -> None:
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.client = Client()
        self.user = get_user_model().objects.create_user(**self.data_of_user)

        # Create a Resume
        ## Create a Mock
        self.resume_pdf_mock = mock.MagicMock(spec=File)
        self.resume_pdf_mock.name = "test.pdf"
        ## Create a Resume
        self.text = "test text"
        self.resume_model = Resume(resume_file=self.resume_pdf_mock, text=self.text, author=self.user)
        
        return super().setUp()


    def test_home_view(self):
        response_of_get = self.client.get(reverse('resumes:home'))
        self.assertEqual(response_of_get.status_code, 200)
        self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')
        print(response_of_get)


    def test_resume_listview(self):
        url = reverse('resumes:resume_list')
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)


    def test_user_resume_listview(self):
        url = reverse('resumes:user_resumes', args={self.user.username})
        #print("the url:", url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)


    def test_resume_detailview(self):
        url = reverse('resumes:resume_detail', args={10})
        #print("the url:", url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 404)


    def test_resume_create_view(self):
        # login
        response_of_login = self.client.login(**self.data_of_user)
        #print(response_of_login)
        self.assertTrue(response_of_login)

        # create the body of the request
        request = RequestFactory().post(reverse('resumes:resume_create'), data=self.data_of_user, files={'resume_file': self.resume_pdf_mock},)
        
        # Call the View, Check 200 code
        request.user = self.user
        response_of_post = ResumeCreateView.as_view()(request)
        #print(response_of_post.context_data['form'].errors)
        self.assertEqual(response_of_post.status_code, 200)

        # TODO: Test the form, and the form_valid method.
        #my_form = ResumeForm(data={}, files={'resume_file': self.resume_pdf_mock},)
        #print("is_valid: ",my_form.is_valid()) ### Return False
        #view_form_valid_response = ResumeCreateView().form_valid(form=my_form)

        #print(response_of_post.__dict__)


    """def test_resume_detailview_context_data(self):
        # Create a detail view
        #self.resume_model.save(commit=False)
        request = RequestFactory().get(reverse('resumes:resume_detail', args={'pk': self.resume_model.pk}))

        view = ResumeDetailView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn('resume', context)
        self.assertIn('reviews', context)
        self.assertIn('review_form', context)"""



class ReviewViews(TestCase):
    def setUp(self) -> None:
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.client = Client()
        self.user = get_user_model().objects.create_user(**self.data_of_user)
        return super().setUp()


    
    def test_user_resume_listview(self):
        url = reverse('resumes:user_reviews', args={self.user.username})
        #print("the url:", url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)






