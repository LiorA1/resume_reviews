from accounts.models import CustomUser
from django.test import TestCase
from blog.models import Post, Comment
# Create your tests here.


class BlogModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser(username='testUser', email='test@test.com')
        self.user.set_password('pass')
        self.user.save()

        self.post_data = {
            'title': 'title1',
            'content': 'content1'
        }
        self.post = Post(title=self.post_data["title"], content=self.post_data["content"], author=self.user)
        self.post.save()

        self.comment_data = {
            'text': 'text1'
        }
        self.comment = Comment(post=self.post, text=self.comment_data['text'], author=self.user)
        self.comment.save()

        return super().setUp()

    def test_user_exists(self):
        pass

    def test_post_exists(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)

    def test_comment_exists(self):
        comment_count = Comment.objects.count()
        self.assertEqual(comment_count, 1)

    def test_post_str(self):
        self.assertEqual(str(self.post), f'{self.post_data["title"]}')

    def test_comment_str(self):

        self.assertEqual(str(self.comment), f'comment of {self.user} on "{self.post}" post')
