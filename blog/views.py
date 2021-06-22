from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls.base import reverse
from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post
from django.shortcuts import get_object_or_404, render

# Create your views here.
from resumes.views import owner


def blog_home(request):
    return render(request, 'blog/blog_home.html')


""" Post List Page/View """
class PostListView(owner.OwnerListView):
    model = Post
    ordering = ['-updated_at']


""" Post Detail Page/View """
class PostDetailView(owner.ParentOwnerDetailView):
    model = Post
    child_model = Comment
    child_form = CommentForm

    #def get_context_data(self, **kwargs):
    #    context = super(PostDetailView, self).get_context_data(**kwargs)
    #    # Getting the specific Post Item
    #    pk = self.kwargs['pk']
    #    PostQuery = get_object_or_404(Post, id=pk)
    #    # Get all the existing Comments for the post
    #    comments = Comment.objects.filter(post=PostQuery).order_by('-updated_at')
    #    comment_form = CommentForm()
    #    print(f'typeof: {type(comment_form)}')
    #    print(f'dict: {comment_form.instance.__dict__}')
    #    context = {'post': PostQuery, 'comments': comments, 'comment_form': comment_form}
    #    return context


""" Post Create Page/View """
class PostCreateView(owner.OwnerCreateView):
    model = Post
    form_class = PostForm


""" Post Update Page/View (with TestMixin)"""
class PostUpdateView(owner.OwnerUpdateView, UserPassesTestMixin):
    model = Post
    form_class = PostForm


    def test_func(self) -> bool:
        post_author = self.get_object().author
        if self.request.user == post_author:
            return True
        return False

    def get_success_url(self):
        #print("PostUpdateView:get_success_url")
        #print("pk is:", self.kwargs.get('pk'))
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])



""" Post Delete Page/View """
class PostDeleteView(owner.OwnerDeleteView):
    model = Post




### Comment Views

""" Comment Create Page/View """
class CommentCreateView(owner.ChildOwnerCreateView):
    model = Comment
    form_class = CommentForm

    parent_model = Post
    parent_reverse_prefix = 'blog:post_detail'

    # We got an error ('IntegrityError at /blog/post/2/create_comment/')
    # i.e: django cant find the post on which the user want to comment on..
    #def form_valid(self, form):
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

    #def get_success_url(self):
    #    try:
    #        url = reverse('blog:post_detail', args=[self.parent_pk])
    #    except:
    #        print("self.parent_pk is not defined")
    #        url = super(CommentCreateView, self).get_success_url()
    #    finally:
    #        return url

        

""" Comment Detail Page/View """
class CommentDetailView(owner.OwnerDetailView):
    model = Comment

    

""" Comment Update Page/View """
class CommentUpdateView(owner.OwnerUpdateView):
    model = Comment
    fields = ['text']

    def get_success_url(self):
        #print("CommentUpdateView:get_success_url", f'pk is: {self.kwargs.get('pk')}')
        #print("parent pk is:", self.__dict__)
        return reverse('blog:post_detail', args=[self.object.post_id])


""" Comment Delete Page/View """
class CommentDeleteView(owner.OwnerDeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post_id])
