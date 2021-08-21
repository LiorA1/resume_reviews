from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.conf import settings
# Create your models here.


class PostQuerySet(models.QuerySet):
    def approve(self):
        """Approve one Post instance. Notice: work on the QuerySet not on a model instance"""
        return self.update(status=Post.STATUS_APPROVED)

    def bulk_approve(self):
        """Approve bulk of Post instances."""
        for obj in self:
            obj.status = Post.STATUS_APPROVED
        return self.bulk_update(self, ['status'])


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    STATUS_DRAFT, STATUS_APPROVED = False, True
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_APPROVED, 'Approved')
    )
    status = models.BooleanField(choices=STATUS_CHOICES, default=STATUS_DRAFT)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'comment of {self.author} on "{self.post}" post'
