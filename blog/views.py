from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls.base import reverse
from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post
from django.shortcuts import get_object_or_404, render

# Create your views here.
from resumes.views import owner


def blog_home(request):
    return render(request, 'blog/blog_home.html')


class PostListView(owner.OwnerListView):
    """ Post List Page/View """
    model = Post
    ordering = ['-updated_at']
    queryset = Post.objects.filter(status=Post.STATUS_APPROVED)


class PostDetailView(owner.ParentOwnerDetailView):
    """ Post Detail Page/View """
    model = Post
    queryset = Post.objects.filter(status=Post.STATUS_APPROVED)
    child_model = Comment
    child_form = CommentForm

    # The ParentOwnerDetailView do all of this in an OOP manner:
    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     # Getting the specific Post Item
    #     pk = self.kwargs['pk']
    #     PostQuery = get_object_or_404(Post, id=pk)
    #     # Get all the existing Comments for the post
    #     comments = Comment.objects.filter(post=PostQuery).order_by('-updated_at')
    #     comment_form = CommentForm()
    #     print(f'typeof: {type(comment_form)}')
    #     print(f'dict: {comment_form.instance.__dict__}')
    #     context = {'post': PostQuery, 'comments': comments, 'comment_form': comment_form}
    #     return context


class PostCreateView(owner.OwnerCreateView):
    """ Post Create Page/View """
    model = Post
    form_class = PostForm


class PostUpdateView(owner.OwnerUpdateView, UserPassesTestMixin):
    """ Post Update Page/View (with TestMixin)"""
    model = Post
    queryset = Post.objects.filter(status=Post.STATUS_APPROVED)
    form_class = PostForm

    def test_func(self) -> bool:
        post_author = self.get_object().author
        if self.request.user == post_author:
            return True
        return False

    def get_success_url(self):
        # print("PostUpdateView:get_success_url")
        # print(f'pk is: {self.kwargs.get("pk")}')
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])


class PostDeleteView(owner.OwnerDeleteView):
    """ Post Delete Page/View """
    model = Post


# ## Comment Views


class CommentCreateView(owner.ChildOwnerCreateView):
    """ Comment Create Page/View """
    model = Comment
    form_class = CommentForm

    parent_model = Post
    parent_reverse_prefix = 'blog:post_detail'

    # The ChildOwnercreate do all of this in an OOP manner:
    # We got an error ('IntegrityError at /blog/post/2/create_comment/')
    # i.e: django cant find the post on which the user want to comment on..
    # def form_valid(self, form):
    #    try:
    #        post_pk = self.kwargs.get('pk', None)
    #        self.success_url=reverse_lazy(f'blog:post_detail', args=[post_pk])
    #        currentPost = get_object_or_404(Post, id=post_pk)
    #        form.instance.post = currentPost
    #    except Exception as e:
    #        print("==============")
    #        print(e, type(e))
    #        print("==============")
    #    return super(CommentCreateView, self).form_valid(form)

    # def get_success_url(self):
    #    try:
    #        url = reverse('blog:post_detail', args=[self.parent_pk])
    #    except:
    #        print("self.parent_pk is not defined")
    #        url = super(CommentCreateView, self).get_success_url()
    #    finally:
    #        return url


class CommentDetailView(owner.OwnerDetailView):
    """ Comment Detail Page/View """
    model = Comment


class CommentUpdateView(owner.OwnerUpdateView):
    """ Comment Update Page/View """
    model = Comment
    fields = ['text']

    def get_success_url(self):
        # print("CommentUpdateView:get_success_url", f'pk is: {self.kwargs.get('pk')}')
        # print("parent pk is:", self.__dict__)
        return reverse('blog:post_detail', args=[self.object.post_id])


class CommentDeleteView(owner.OwnerDeleteView):
    """ Comment Delete Page/View """
    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post_id])
