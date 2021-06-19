from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.


from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import ListView
from accounts.models import CustomUser

from resumes.models import Review, Resume
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


""" Review List Page/View """
class ReviewListView(OwnerListView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_list.html"


""" Review User List Page/View """
class UserReviewListView(ListView):
    model = Review
    template_name = 'resumes/user_reviews.html'
    #context_object_name = 'reviews'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        return Review.objects.filter(author=user).order_by('-id')


""" Review Detail Page/View """
class ReviewDetailView(OwnerDetailView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_detail.html"


""" Review Create Page/View """
class ReviewCreateView(OwnerCreateView):
    model = Review
    fields = ['grade', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"
    
    
    def form_valid(self, form):
        #print("ReviewCreateView:form_valid")

        # Define 2 ForeignKey(s) inside a createview
        # Examples:
        #  form.instance.author = self.request.user
        #  form.instance.grade = self.request.POST.get('grade', None)
        # https://stackoverflow.com/a/53639341/3790620

        # Need to assign the parent object (ForeignKey) in the form
        try:
            resume_pk = self.kwargs.get('pk', None)
            self.success_url=reverse_lazy(f'resumes:resume_detail', args=[resume_pk])
            currentResume = get_object_or_404(Resume, id=resume_pk)
            # Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.
            form.instance.resume = currentResume
        except Exception as e:
            print("ReviewCreateView:form_valid:Exception:\n", e, type(e))
        

        return super(ReviewCreateView, self).form_valid(form)



""" Review Update Page/View """
class ReviewUpdateView(OwnerUpdateView):
    model = Review
    fields = ['grade', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"

    def get_success_url(self):
        #print("CommentUpdateView:get_success_url")
        #print("pk is:", self.kwargs.get('pk'))
        #print("kwargs is:", self.kwargs)
        #print("parent pk is:", self.object.resume_id)
        return reverse('resumes:resume_detail', args=[self.object.resume_id])


""" Review Delete Page/View """
class ReviewDeleteView(OwnerDeleteView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_confirm_delete.html"

    def get_success_url(self):
        return reverse('resumes:resume_detail', args=[self.object.resume_id])
