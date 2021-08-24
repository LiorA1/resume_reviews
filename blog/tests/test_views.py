from typing import List
from django.db.models.query_utils import Q
from blog.models import Comment, Post
from blog.views import CommentCreateView, PostCreateView
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseBase
from django.urls import reverse


class BlogViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        return super().setUpTestData()

    def setUp(self) -> None:

        self.client = Client()

        self.data_of_user = {
            'username': 'test_user1',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }

        self.user = get_user_model().objects.create_user(**self.data_of_user)

        self.data_of_user_2 = {
            'username': 'test_user2',
            'password': 'thndjg5395hj',
            'email': 'test2@test.com',
        }

        self.user_2 = get_user_model().objects.create_user(**self.data_of_user_2)

        return super().setUp()

    def create_post(self, title: str, content: str, author) -> HttpResponseBase:
        '''Create a Post'''

        post_data = {
            "title": title,
            "content": content,
            "author": author,
        }

        # create a request
        url_post_create = reverse('blog:post_create')
        request = RequestFactory().post(url_post_create, data=post_data, format="multipart")
        request.user = author

        # Execute a call for ResumeCreateView
        response_of_post = PostCreateView.as_view()(request)

        return response_of_post

    def create_comment(self, text: str, post_id: int) -> HttpResponseBase:
        '''Create a Comment'''
        comment_data = {
            'text': text,
        }

        url = reverse('blog:comment_create', args={post_id})
        req = RequestFactory().post(path=url, data=comment_data)
        req.user = self.user

        kwargs = {'pk': post_id}

        res = CommentCreateView.as_view()(req, **kwargs)

        return res


class PostViewTest(BlogViewsTest):

    def test_post_listview_reachable(self):
        '''Test post listview can be reached'''
        url = reverse('blog:post_list')
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)

    # def test_user_post_listview(self):
    #     url = reverse('blog:user_posts', args={self.user.username})
    #     #print("the url:", url)
    #     response_of_get = self.client.get(url)
    #     self.assertEqual(response_of_get.status_code, 200)

    def test_post_create_delete(self):
        '''Test post create and delete processes'''
        response_of_login = self.client.login(**self.data_of_user)

        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        self.assertEqual(response_of_post.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        # # Check deletion of resume (review need to be deleted as well)
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.post(url_delete, follow=True)

        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_post_valid_user_update(self):
        '''Test post create and delete processes'''
        response_of_login = self.client.login(**self.data_of_user)

        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        self.assertEqual(response_of_post.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        Post.objects.all().bulk_approve()
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        # updateview
        url_update = reverse('blog:post_update', args={1})
        response_of_update_get = self.client.get(url_update)
        self.assertEqual(response_of_update_get.status_code, 200)

        data = {
            'title': "modified post title",
            'content': "modified post content",
        }
        response_of_update_post = self.client.post(url_update, data=data)

        response_of_redirect = self.client.get(response_of_update_post.url)

        self.assertEqual(response_of_redirect.status_code, 200)
        self.assertEqual(response_of_redirect.context['post'].title, data.get('title'))
        self.assertEqual(response_of_redirect.context['post'].content, data.get('content'))

        # python manage.py test blog.tests.test_views.PostViewTest

        # delete post
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.post(url_delete, follow=True)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_post_anon_user_update(self):
        '''Test post create and delete processes'''
        response_of_login = self.client.login(**self.data_of_user)
        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        self.assertEqual(response_of_post.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        Post.objects.all().bulk_approve()
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        self.client.logout()

        # updateview
        url_update = reverse('blog:post_update', args={1})
        response_of_update_get = self.client.get(url_update)
        self.assertEqual(response_of_update_get.status_code, 302)

        response_of_redirect = self.client.get(response_of_update_get.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        data = {
            'title': "modified post title",
            'content': "modified post content",
        }
        response_of_update_post = self.client.post(url_update, data=data)
        self.assertEqual(response_of_update_post.status_code, 302)

        # python manage.py test blog.tests.test_views.PostViewTest

        response_of_login = self.client.login(**self.data_of_user)

        # # Check deletion of resume (review need to be deleted as well)
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.post(url_delete, follow=True)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_post_other_user_update(self):
        '''Test post create and delete processes'''
        response_of_login = self.client.login(**self.data_of_user)

        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        self.assertEqual(response_of_post.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        Post.objects.all().bulk_approve()
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user_2)

        # updateview
        url_update = reverse('blog:post_update', args={1})
        response_of_update_get = self.client.get(url_update)
        self.assertEqual(response_of_update_get.status_code, 404)

        data = {
            'title': "modified post title",
            'content': "modified post content",
        }
        response_of_update_post = self.client.post(url_update, data=data)
        self.assertEqual(response_of_update_post.status_code, 404)

        # python manage.py test blog.tests.test_views.PostViewTest

        self.client.logout()
        response_of_login = self.client.login(**self.data_of_user)

        # delete the post
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.post(url_delete, follow=True)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_post_approve_functionality(self):
        response_of_login = self.client.login(**self.data_of_user)

        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 404)
        Post.objects.all().bulk_approve()
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

    def _check_search_finctionality(self, search_term_given: str, posts_pk: List = None):
        '''Checks that the search function, works as expected.'''
        url = reverse('blog:post_list')
        data = {"search": search_term_given}
        response_of_get = self.client.get(url, data=data)
        self.assertEqual(response_of_get.status_code, 200)

        # Get the posts directly from the DB.
        query_title_and_text = Q(title__icontains=search_term_given) | Q(content__icontains=search_term_given) 
        post_ids_from_db = Post.objects.filter(query_title_and_text).values_list('pk', flat=True)

        Post.objects.all().bulk_approve()
        response_of_get = self.client.get(url, data=data)

        # Get the posts from the view.
        id_set = set()
        for post in response_of_get.context['post_list']:
            id_set.add(post.pk)

        # Check that the two sets are equal
        self.assertTrue(id_set == set(post_ids_from_db))

        set_of_posts_id = set()
        if posts_pk:
            i_posts_pk = list()
            for pk in posts_pk:
                self.assertTrue(pk in post_ids_from_db)
                set_of_posts_id.add(pk)

    def test_post_listview_search_option(self):
        '''Test if the post listview search function, works as expected.'''
        response_of_login = self.client.login(**self.data_of_user)

        self.assertEqual(Post.objects.count(), 0)
        response_of_post = self.create_post("title for first post test", "content for first post", self.user)
        first_post_id = 1
        self.assertEqual(Post.objects.count(), 1)
        response_of_post = self.create_post("second post for title", "content of the second post", self.user)
        second_post_id = 2
        self.assertEqual(Post.objects.count(), 2)
        response_of_post = self.create_post("third post title", "content of the third post", self.user)
        third_post_id = 3
        self.assertEqual(Post.objects.count(), 3)

        first_post_id_l = [first_post_id]
        self._check_search_finctionality("title for first", first_post_id_l)
        self._check_search_finctionality("first post", first_post_id_l)

        all_posts_id = [first_post_id, second_post_id, third_post_id]
        self._check_search_finctionality("title", all_posts_id)
        self._check_search_finctionality("content", all_posts_id)

        f_s_list = [first_post_id, second_post_id]
        self._check_search_finctionality(" for", f_s_list)
        s_t_list = [second_post_id, third_post_id]
        self._check_search_finctionality("of ", s_t_list)

        #
        # python manage.py test blog.tests.test_views.PostViewTest
        #

    def test_post_detailview(self):
        ''' Test the DetailView after Post creation'''
        response_of_login = self.client.login(**self.data_of_user)

        # # Create a Post
        post_title = "title for post test"
        post_content = "content for a test post"
        response_of_post = self.create_post(title=post_title, content=post_content, author=self.user)

        self.assertEqual(Post.objects.count(), 1)  # # Check that a Post been created
        self.assertEqual(response_of_post.status_code, 302)  # # Check status Code is 302 (Redirect)

        # # Check detailView path was created
        url = reverse('blog:post_detail', args={1})
        self.assertEqual(response_of_post.url, url)

        # # Check 404 Code after the redirect (before approved)
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 404)

        # # Check 200 Code after the redirect (after approved)
        Post.objects.all().approve()
        response_of_redirect = self.client.get(response_of_post.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        # # Check we in detailview template
        self.assertTemplateUsed(response_of_redirect, 'blog/post_detail.html')

        # # Check context members exists
        self.assertIsNotNone(response_of_redirect.context['post'])
        self.assertIsNotNone(response_of_redirect.context['comments'])
        self.assertIsNotNone(response_of_redirect.context['comment_form'])

        self.assertEqual(str(response_of_redirect.context['post']), post_title)

        # # Check deletion of post
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.get(url_delete)

        # # Check template
        self.assertTemplateUsed(response_of_delete, 'blog/post_confirm_delete.html')

        # # Check deletion of post
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Post.objects.count(), 0)


class CommentViewTest(BlogViewsTest):

    def test_comment_create_delete(self):
        """Test the creation and deletion of a comment"""
        # login
        response_of_login = self.client.login(**self.data_of_user)

        # # Create a Post
        post_title = "title for post test"
        post_content = "content for a test post"
        response_of_post = self.create_post(title=post_title, content=post_content, author=self.user)
        # Check that a Post been created
        self.assertEqual(Post.objects.count(), 1)

        comment_text = "this is a great post"
        post_id = 1
        response_of_create_comment = self.create_comment(comment_text, post_id)

        # # Check item been created and saved
        self.assertEqual(Comment.objects.count(), 1)

        # # Check status Code is 302 (Redirect)
        self.assertEqual(response_of_create_comment.status_code, 302)

        # # Check item exists in his parent detail view
        # # Check detailView path was created
        url = reverse('blog:post_detail', args={post_id})
        self.assertEqual(response_of_create_comment.url, url)

        # # Check 404 Code after the redirect (before approved)
        response_of_redirect = self.client.get(response_of_create_comment.url)
        self.assertEqual(response_of_redirect.status_code, 404)

        # # Check 200 Code after the redirect and aaproved.
        Post.objects.all().bulk_approve()
        response_of_redirect = self.client.get(response_of_create_comment.url)
        self.assertEqual(response_of_redirect.status_code, 200)

        self.assertEqual(response_of_redirect.context['comments'].count(), 1)

        # # Check deletion of comment
        comment_id = 1
        url_delete = reverse('blog:comment_delete', args={comment_id})
        response_of_delete = self.client.get(url_delete)

        # # Check template
        self.assertTemplateUsed(response_of_delete, 'blog/comment_confirm_delete.html')

        # # Check deletion of comment
        response_of_delete = self.client.post(url_delete)
        # print(f'response_of_delete: {response_of_delete}')
        self.assertEqual(Comment.objects.count(), 0)

        # ! Clean AWS
        url_delete = reverse('blog:post_delete', args={post_id})
        response_of_delete = self.client.post(url_delete)

    def test_comment_deletion_via_post_deletion(self):
        """Test the removal of comment, when its parent is removed"""

        response_of_login = self.client.login(**self.data_of_user)

        post_id = 1
        # # Create a Post
        post_title = "title for post test"
        post_content = "content for a test post"
        response_of_post = self.create_post(title=post_title, content=post_content, author=self.user)
        # Check that a Post been created
        self.assertEqual(Post.objects.count(), 1)

        comment_id = 1
        comment_text = "this is a great post"
        response_of_create_comment = self.create_comment(comment_text, post_id)

        # ## Check deletion of comment when parent post deleted

        self.assertEqual(Comment.objects.count(), 1)

        url_delete = reverse('blog:post_delete', args={post_id})
        response_of_delete = self.client.post(url_delete)

        self.assertEqual(Comment.objects.count(), 0)

        # # Check parent item removal
        self.assertEqual(Post.objects.count(), 0)
