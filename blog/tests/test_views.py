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
        self.data_of_user = {
            'username': 'test',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.client = Client()
        self.user = get_user_model().objects.create_user(**self.data_of_user)

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

    def test_post_listview(self):
        url = reverse('blog:post_list')
        response_of_get = self.client.get(url)
        self.assertEqual(response_of_get.status_code, 200)

    # def test_user_post_listview(self):
    #     url = reverse('blog:user_posts', args={self.user.username})
    #     #print("the url:", url)
    #     response_of_get = self.client.get(url)
    #     self.assertEqual(response_of_get.status_code, 200)

    def test_post_create_delete(self):
        # # login
        response_of_login = self.client.login(**self.data_of_user)

        # # Create a Post
        response_of_post = self.create_post("title for post test", "content for a test post", self.user)

        # # Check status Code is 302 (Redirect)
        self.assertEqual(response_of_post.status_code, 302)

        # # Check that a Resume been created
        self.assertEqual(Post.objects.count(), 1)

        # # Check deletation of resume (review need to be deleted as well)
        url_delete = reverse('blog:post_delete', args={1})
        response_of_delete = self.client.post(url_delete, follow=True)

        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response_of_delete.status_code, 200)

    def test_post_detailview(self):
        # login
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
