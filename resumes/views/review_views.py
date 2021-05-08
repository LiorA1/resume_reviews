from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.


from django.urls import reverse_lazy
from django.views.generic import ListView
from accounts.models import CustomUser

from resumes.models import Review, Resume
from resumes.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class ReviewListView(OwnerListView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_list.html"

    #TODO: this will give you all the reviews, you need to get the reviews of a specific Resume


class UserReviewListView(ListView):
    model = Review
    template_name = 'resumes/user_reviews.html'
    #context_object_name = 'reviews'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        return Review.objects.filter(author=user).order_by('-id')


class ReviewDetailView(OwnerDetailView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_detail.html"


class ReviewCreateView(OwnerCreateView):
    model = Review
    fields = ['grade', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"
    
    # https://stackoverflow.com/a/53639341/3790620
    """"""
    def form_valid(self, form):
        print("form_valid called from review_views file")

        #form.instance.author = self.request.user
        #form.instance.grade = self.request.POST.get('grade', None)
        #form.instance.text = self.request.POST.get('text', None)

        try:
            resume_pk = self.kwargs.get('pk', None)
            self.success_url=reverse_lazy(f'resumes:resume_detail', args=[resume_pk])
            currentResume = get_object_or_404(Resume, id=resume_pk)
            # Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.
            form.instance.resume = currentResume
        except Exception as e:
            print("==============")
            print(e, type(e))
            print("==============")
        

        #TODO: consider to add review form in the resume detail page/view
        #! Done.

        return super(ReviewCreateView, self).form_valid(form)






class ReviewUpdateView(OwnerUpdateView):
    model = Review
    fields = ['grade', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"


class ReviewDeleteView(OwnerDeleteView):
    model = Review
    # By convention:
    # template_name = "resumes/<modelName>_confirm_delete.html"
