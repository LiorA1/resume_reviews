from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'resumes/home.html')


from resumes.models import Resume, Review
from resumes.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views.generic import ListView

from ..forms import ReviewForm

from accounts.models import CustomUser

class ResumeListView(OwnerListView):
    model = Resume
    # By convention:
    # template_name = "resumes/<modelName>_list.html"


class UserResumeListView(ListView):
    model = Resume
    template_name = 'resumes/user_resumes.html'
    #context_object_name = 'resumes'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        return Resume.objects.filter(author=user).order_by('-id')


class ResumeDetailView(OwnerDetailView):
    model = Resume
    # By convention:
    # template_name = "resumes/<modelName>_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        resumeQuery = get_object_or_404(Resume, id=pk) #! Getting the Specific Resume

        reviews = Review.objects.filter(resume=resumeQuery).order_by('-updated_at') #! Get all the comments belongs to the Resume
        review_form = ReviewForm()
        context = { 'resume': resumeQuery, 'reviews': reviews, 'review_form': review_form}

        return context




class ResumeCreateView(OwnerCreateView):
    model = Resume
    fields = ['resume_file', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"
    #success_url = reverse_lazy(f'{app_name}:all')


class ResumeUpdateView(OwnerUpdateView):
    model = Resume
    fields = ['resume_file', 'text']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"


class ResumeDeleteView(OwnerDeleteView):
    model = Resume
    # By convention:
    # template_name = "resumes/<modelName>_confirm_delete.html"
