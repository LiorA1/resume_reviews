from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from resumes.views.review_views import ReviewCreateView
from resumes.forms import ResumeForm, ReviewForm
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..views import ResumeCreateView, ResumeCreateView, ResumeDetailView
from ..models import Resume, Review

from unittest import mock
from django.core.files import File

# Objectives:
# 0. Test home view
# 1. Test OwnerCreateView
# 2. Test ResumeUpdateView
# 3. Test ResumeDeleteView

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#views

import os.path


class ResumesViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        FOLDER_NAME = 'data'
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        cls.TEST_DATA_DIR = os.path.join(TEST_DIR, FOLDER_NAME)

        return super().setUpTestData()

    def setUp(self) -> None:
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.client = Client()
        self.user = get_user_model().objects.create_user(**self.data_of_user)

        return super().setUp()

    def create_resume(self, text: str, file_path: str, author) -> HttpResponseBase:
        '''Create a Resume'''

        from django.core.files.uploadedfile import SimpleUploadedFile

        # print(f'create_resume, file path: |{file_path}|')

        resume_data = {
            "text": text,
            "author": author,
        }

        # create a request
        with open(file_path, 'rb') as fhandler:
            resume_data['resume_file'] = SimpleUploadedFile(
                name="resume_sample.pdf",
                content=fhandler.read(),
                content_type="application/pdf")

            url_post_create = reverse('resumes:resume_create')
            request = RequestFactory().post(url_post_create, data=resume_data, format="multipart")
            request.user = author

        # Execute a call for ResumeCreateView
        response_of_post = ResumeCreateView.as_view()(request)

        return response_of_post

    def create_review(self, grade: int, text: str, resume_id: int) -> HttpResponseBase:
        '''Create a Review'''
        data_for_review = {
            'grade': grade,
            'text': text,
        }

        url = reverse('resumes:review_create', args={resume_id})
        req = RequestFactory().post(path=url, data=data_for_review)
        req.user = self.user

        kwargs = {'pk': resume_id}

        res = ReviewCreateView.as_view()(req, **kwargs)

        return res


class ResumeViews(ResumesViewsTest):

    # def test_home_view(self):
    #     url = reverse('resumes:home')
    #     response_of_get = self.client.get(url)
    #     self.assertEqual(response_of_get.status_code, 200)
    #     self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')

    def test_resume_listview(self):
        url = reverse('resumes:resume_list')
        response_of_get = self.client.get(url)
        # print(response_of_get.content)
        self.assertEqual(response_of_get.status_code, 200)

    def test_user_resume_listview(self):
        url = reverse('resumes:user_resumes', args={self.user.username})
        # print("the url:", url)
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)

    def test_resume_create_delete(self):
        # # login
        response_of_login = self.client.login(**self.data_of_user)

        # # Create a file
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        # # Create a Resume
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user)

        # # Check status Code is 302 (Redirect)
        self.assertEqual(response_of_post.status_code, 302)

        # # Check that a Resume been created
        self.assertEqual(Resume.objects.count(), 1)

        # # Check deletation of resume (review need to be deleted as well)
        resume_id = 1
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete, follow=True)

        self.assertEqual(Resume.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_resume_detailview(self):
        # login
        response_of_login = self.client.login(**self.data_of_user)

        # Create a file
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')

        # # create resume
        response_of_post = self.create_resume("text for sample resume test", pdf_file_path, self.user)

        self.assertEqual(Resume.objects.count(), 1)  # # Check that a Resume been created
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)

        # # Check detailView path was created
        resume_id = 1
        url = reverse('resumes:resume_detail', args={resume_id})
        self.assertEqual(response_of_post.url, url)

        # # Check 200 Code after the redirect
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        # # Check we in detailview template
        self.assertTemplateUsed(response_of_redirect, 'resumes/resume_detail.html')

        # # Check context members exists
        self.assertIsNotNone(response_of_redirect.context['resume'])
        self.assertIsNotNone(response_of_redirect.context['reviews'])
        self.assertIsNotNone(response_of_redirect.context['review_form'])

        # # Check deletion of resume
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.get(url_delete)

        # # Check template
        self.assertTemplateUsed(response_of_delete, 'resumes/resume_confirm_delete.html')

        # # Check deletion of resume
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)


class ReviewViews(ResumesViewsTest):

    def test_review_create_delete(self):
        """Test the creation and deletion of a review"""
        # login
        response_of_login = self.client.login(**self.data_of_user)

        # Create a file
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        # Create a Resume
        resume_id = 1
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user)

        # Check that a Resume been created
        self.assertEqual(Resume.objects.count(), 1)

        review_id = 1
        response_of_create_review = self.create_review(5, "Mary resume is better", 1)

        # # Check item been created and saved
        self.assertEqual(Review.objects.count(), 1)

        # # Check status Code is 302 (Redirect)
        self.assertEqual(response_of_create_review.status_code, 302)

        # # Check item exists in his parent detail view
        # # Check detailView path was created
        url = reverse('resumes:resume_detail', args={resume_id})
        self.assertEqual(response_of_create_review.url, url)

        # # Check 200 Code after the redirect
        response_of_redirect = self.client.get(response_of_create_review.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        self.assertEqual(response_of_redirect.context['reviews'].count(), 1)

        # # Check deletion of review
        url_delete = reverse('resumes:review_delete', args={review_id})
        response_of_delete = self.client.get(url_delete)

        # # Check template
        self.assertTemplateUsed(response_of_delete, 'resumes/review_confirm_delete.html')

        # # Check deletion of review
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Review.objects.count(), 0)


        # ! Clean AWS
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)

    def test_review_deletion_via_resume_deletion(self):
        """Test the removal of review, when its parent is removed"""

        response_of_login = self.client.login(**self.data_of_user)

        # Create a file
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        resume_id = 1
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user)

        # Check that a Resume been created
        self.assertEqual(Resume.objects.count(), 1)

        review_id = 1
        response_of_create_review = self.create_review(5, "Mary resume is better", 1)

        # ## Check deletion of review when parent resume deleted

        self.assertEqual(Review.objects.count(), 1)

        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)

        self.assertEqual(Review.objects.count(), 0)

        # # Check parent item removal
        self.assertEqual(Resume.objects.count(), 0)
