from django.shortcuts import get_object_or_404
# Create your views here.


from django.urls import reverse
from django.urls.base import reverse
from django.views.generic import ListView
from accounts.models import CustomUser

from resumes.models import Review, Resume
from .owner import OwnerListView, OwnerDetailView,\
     OwnerCreateView, OwnerUpdateView, OwnerDeleteView, ChildOwnerCreateView


class ReviewListView(OwnerListView):
    """ Review List Page/View """
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_list.html"


class UserReviewListView(ListView):
    """ Review User List Page/View """
    model = Review
    template_name = 'resumes/user_reviews.html'
    # context_object_name = 'reviews'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        return Review.objects.filter(author=user).order_by('-id')


class ReviewDetailView(OwnerDetailView):
    """ Review Detail Page/View """
    model = Review
    # template_name = "resumes/<modelName>_detail.html"


class ReviewCreateView(ChildOwnerCreateView):
    """ Review Create Page/View """
    model = Review
    fields = ['grade', 'text']
    # template_name = "resumes/<modelName>_form.html"

    parent_model = Resume
    parent_reverse_prefix = 'resumes:resume_detail'

    # # The ChildOwnercreate do all of this in an OOP manner:
    # def form_valid(self, form):
    #     # print("ReviewCreateView:form_valid")
    #     # Define 2 ForeignKey(s) inside a createview
    #     # Example:
    #     #  form.instance.grade = self.request.POST.get('grade', None)
    #     # https://stackoverflow.com/a/53639341/3790620
    #     # Assign the parent object (ForeignKey) in the form
    #     try:
    #         resume_pk = self.kwargs.get('pk', None)
    #         self.success_url = reverse(f'resumes:resume_detail', args=[resume_pk])
    #         currentResume = get_object_or_404(Resume, id=resume_pk)
    #         # Calls get() on a given model manager,\
    #         #  but it raises Http404 instead of the model’s DoesNotExist exception.
    #         form.instance.resume = currentResume
    #     except Exception as e:
    #         print("ReviewCreateView:form_valid:Exception:\n", e, type(e))
    #     return super(ReviewCreateView, self).form_valid(form)


class ReviewUpdateView(OwnerUpdateView):
    """ Review Update Page/View """
    model = Review
    fields = ['grade', 'text']

    def get_success_url(self):
        # print("CommentUpdateView:get_success_url", f"pk is: {self.kwargs.get('pk')}")
        # print("parent pk is:", self.object.resume_id)
        return reverse('resumes:resume_detail', args=[self.object.resume_id])


class ReviewDeleteView(OwnerDeleteView):
    """ Review Delete Page/View """
    model = Review
    # template_name = "resumes/<modelName>_confirm_delete.html"

    def get_success_url(self):
        return reverse('resumes:resume_detail', args=[self.object.resume_id])
