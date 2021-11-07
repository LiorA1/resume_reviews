import time
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from resumes.views.review_views import ReviewCreateView
from resumes.forms import ResumeForm, ReviewForm
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..views import ResumeCreateView, ResumeCreateView, ResumeDetailView
from ..models import Resume, Review, Tag

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
    '''A Base Class for all View-Test classes, in resume App'''
    @classmethod
    def setUpTestData(cls) -> None:

        FOLDER_NAME = 'data'
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        cls.TEST_DATA_DIR = os.path.join(TEST_DIR, FOLDER_NAME)

        return super().setUpTestData()

    def setUp(self) -> None:
        self.client = Client()

        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.user = get_user_model().objects.create_user(**self.data_of_user)

        self.data_of_user_b = {
            'username': 'test2',
            'password': '274fkvj7sAG4G',
            'email': 'test2@test.com',
        }
        self.user_b = get_user_model().objects.create_user(**self.data_of_user_b)

        return super().setUp()

    def create_resume(self, text: str, file_path: str, author, tags_id: List = None) -> HttpResponseBase:
        """
        Creates a Resume, using SimpleUploadedFile and RequestFactory.
        Returns the POST response.
        """

        from django.core.files.uploadedfile import SimpleUploadedFile

        # print(f'create_resume, file path: |{file_path}|')

        resume_data = {
            "text": text,
            "author": author
        }
        if tags_id:
            resume_data["tags"] = tags_id

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

    def _delete_resume_db(self, resume_id: int):
        url_delete_resume = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete_resume, follow=True)
        self.assertEqual(response_of_delete.status_code, 200)
        return response_of_delete

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

    def _create_tag_db(self, name: str) -> Tag:
        res = Tag.objects.create(name=name)
        return res


class ResumeViews(ResumesViewsTest):
    '''A Test class for all resume_views in resume App'''

    # def test_home_view(self):
    #     url = reverse('resumes:home')
    #     response_of_get = self.client.get(url)
    #     self.assertEqual(response_of_get.status_code, 200)
    #     self.assertTemplateUsed(response_of_get, template_name='resumes/home.html')

    def test_resume_listview_reachable(self):
        '''Test resume listview can be reached'''
        url = reverse('resumes:resume_list')
        response_of_get = self.client.get(url)
        # print(response_of_get.content)
        self.assertEqual(response_of_get.status_code, 200)

    def _check_search_function(self, search_term_given: str, tags_pk: List):
        '''
        Checks if the searchTerm search process yield the same results as expected:\n
        If the string is empty - base case: No AssertionError will be raised.\n
        If the string is not empty - search process need to yield same resumes id's as a db search following the given tags_pk List.\n
        Otherwise - AssertionError will be raised.
        '''

        url = reverse('resumes:resume_list')
        data = {"search": search_term_given}
        response_of_get = self.client.get(url, data=data)
        self.assertEqual(response_of_get.status_code, 200)

        if len(search_term_given) > 0:
            esa_is = []
            # Check that each resume associated with the tags from data
            for resume in response_of_get.context['resume_list']:
                esa_is.append(resume.id)

            resumes_id = Tag.objects.filter(pk__in=tags_pk).values_list('resume__id', flat=True)

            self.assertTrue(set(resumes_id) == set(esa_is))
        else:
            resumes_in_db_count = Resume.objects.count()
            resumes_in_response = len(response_of_get.context['resume_list'])
            self.assertTrue(resumes_in_db_count == resumes_in_response)

    def test_resume_listview_search_function(self):
        '''Test if the search bar (string) function as excpected.'''
        # login
        response_of_login = self.client.login(**self.data_of_user)

        # # Create a file
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        # # Creates 3 Tags
        java_tag = self._create_tag_db("Java")
        python_tag = self._create_tag_db("Python")
        c_tag = self._create_tag_db("C")

        # # Create 3 Resumes
        tags = [java_tag.pk, python_tag.pk]
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user, tags)
        self.assertEqual(Resume.objects.count(), 1)
        tags = [java_tag.pk, python_tag.pk, c_tag.pk]
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user, tags)
        self.assertEqual(Resume.objects.count(), 2)
        tags = [java_tag.pk, c_tag.pk]
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user, tags)
        self.assertEqual(Resume.objects.count(), 3)

        # check a string that not contains any tag name - Return empty list of resumes.
        empty_id_list = []
        self._check_search_function("PyThOny", empty_id_list)

        # check a string that contains one tag name - Return only relevant resumes.
        python_id_list = [python_tag.pk]
        self._check_search_function("PyThOn", python_id_list)

        # check a string that contains two tag names - Return only relevant resumes.
        python_java_id_list = [python_tag.pk, java_tag.pk]
        self._check_search_function("PyThOn jaVa", python_java_id_list)

        # check empty string - Return all Resumes.
        all_id_list = []
        self._check_search_function("", all_id_list)

        # # Check deletion of resume (review need to be deleted as well)
        self.assertEqual(Resume.objects.count(), 3)
        response_of_delete = self._delete_resume_db(1)
        self.assertEqual(Resume.objects.count(), 2)

        response_of_delete = self._delete_resume_db(2)
        self.assertEqual(Resume.objects.count(), 1)

        response_of_delete = self._delete_resume_db(3)
        self.assertEqual(Resume.objects.count(), 0)

        # docker exec -it django_container_slim_resume_viewer sh
        # python manage.py test resumes.tests.test_views.ResumeViews.test_resume_listview_search_function

    def test_user_resume_listview_reachable(self):
        '''Test if the user resume listview is reachable'''
        url = reverse('resumes:user_resumes', args={self.user.username})
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)

    def test_resume_create_delete_loggedin(self):
        '''Test resume create and delete processes'''
        response_of_login = self.client.login(**self.data_of_user)

        # Create a file path
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        # Create a Resume
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user)

        # Check status Code is 302 (Redirect) - creation success
        self.assertEqual(response_of_post.status_code, 302)

        # Check that a Resume been created
        self.assertEqual(Resume.objects.count(), 1)

        # Check deletion of resume (review need to be deleted as well)
        resume_id = 1
        url_delete = reverse('resumes:resume_delete', args={resume_id})

        # Check confirmation template is used
        response_of_delete = self.client.get(url_delete)
        self.assertTemplateUsed(response_of_delete, 'resumes/resume_confirm_delete.html')

        response_of_delete = self.client.post(url_delete, follow=True)
        self.assertEqual(Resume.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_resume_detailview_loggedin(self):
        ''' Test the DetailView after resume creation'''
        response_of_login = self.client.login(**self.data_of_user)

        # Create a file
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')

        # # create resume
        response_of_post = self.create_resume("text for sample resume test", pdf_file_path, self.user)
        self.assertEqual(Resume.objects.count(), 1)  # # Check that a Resume been created
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)

        # # Check detailView path was created, and is redirected at
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

        # deletion of resume
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)

    def test_resume_update_reachable(self):
        ''' Test the UpdateView after resume creation'''
        response_of_login = self.client.login(**self.data_of_user)

        # Create Resume
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')
        response_of_post = self.create_resume("text for sample resume test", pdf_file_path, self.user)
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)
        self.assertEqual(Resume.objects.count(), 1)  # # Check that a Resume been created

        # # Check updateView path was created
        resume_id = 1
        url = reverse('resumes:resume_update', args={resume_id})

        # GET UpdateView path
        response_of_redirect = self.client.get(url)
        self.assertEqual(response_of_redirect.status_code, 200)

        # delete
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)

        # python manage.py test resumes.tests.test_views.ResumeViews

    #
    def test_resume_update_post(self):
        """
        Test the UpdateView for the author.
        """

        response_of_login = self.client.login(**self.data_of_user)

        # Create Resume
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')
        response_of_post = self.create_resume("text for sample resume test", pdf_file_path, self.user)
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)
        self.assertEqual(Resume.objects.count(), 1)  # # Check that a Resume been created

        # # Check updateView path was created
        resume_id = 1
        url = reverse('resumes:resume_update', args={resume_id})

        resume_data = {
            "text": "text updated",
        }

        # POST UpdateView path
        response_of_post = self.client.post(url, resume_data)
        self.assertEqual(response_of_post.status_code, 302)

        # follow the rediredct
        # # Check 200 Code after the redirect
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        # Check "text updated" apperance
        self.assertEqual(response_of_redirect.context_data['resume'].text, resume_data['text'])

        # delete
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)

        # python manage.py test resumes.tests.test_views.ResumeViews.test_resume_update_post

    def test_resume_userb_update_usera_resume(self):
        """
        Test the UpdateView for a different loggedin user.
        """

        response_of_login = self.client.login(**self.data_of_user)

        # Create Resume
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')
        response_of_post = self.create_resume("text for sample resume test", pdf_file_path, self.user)
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)
        self.assertEqual(Resume.objects.count(), 1)  # # Check that a Resume been created

        # Check updateView
        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user_b)
        resume_id = 1
        url = reverse('resumes:resume_update', args={resume_id})

        resume_data = {
            "text": "text updated",
        }

        # POST UpdateView path
        response_of_post = self.client.post(url, resume_data)
        self.assertEqual(response_of_post.status_code, 404)

        # delete
        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user)
        url_delete = reverse('resumes:resume_delete', args={resume_id})
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)

        # python manage.py test resumes.tests.test_views.ResumeViews.test_resume_userb_update_usera_resume

    #
    def test_resume_userb_to_delete_usera_resume(self):
        """
        Test the DeleteView for a different loggedin user.
        """

        response_of_login = self.client.login(**self.data_of_user)

        # Create a file path
        FILE_NAME = 'resume_sample.pdf'
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, FILE_NAME)

        # Create a Resume
        response_of_post = self.create_resume("text for resume test", pdf_file_path, self.user)

        # Check status Code is 302 (Redirect) - creation success
        self.assertEqual(response_of_post.status_code, 302)

        # Check that a Resume been created
        self.assertEqual(Resume.objects.count(), 1)

        # Attempt of user_b to delete resume of user
        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user_b)
        resume_id = 1
        url_delete = reverse('resumes:resume_delete', args={resume_id})

        # Check confirmation template is used
        response_of_delete = self.client.get(url_delete)
        #self.assertTemplateUsed(response_of_delete, 'resumes/resume_confirm_delete.html')

        response_of_delete = self.client.post(url_delete, follow=True)
        self.assertEqual(response_of_delete.status_code, 404)
        self.assertEqual(Resume.objects.count(), 1)

        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user)

        # deletion of resume
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Resume.objects.count(), 0)

        # python manage.py test resumes.tests.test_views.ResumeViews


class ReviewViews(ResumesViewsTest):
    '''A Test class for all review_views in resume App'''

    def test_review_create_delete(self):
        '''Test the creation and deletion of a review'''
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
