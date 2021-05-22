from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'resumes/home.html')


from resumes.models import Resume, Review
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views.generic import ListView

from ..forms import ReviewForm

from accounts.models import CustomUser

#from el_pagination.views import AjaxListView

"""Display all the resumes"""
class ResumeListView(OwnerListView):
    model = Resume
    ordering = ['-created_at']
    #paginate_by = 1
    # By convention:
    # template_name = "resumes/<modelName>_list.html"


#TODO:
"""Create a view that will load Via AJAX resumes objects"""
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#@method_decorator(csrf_exempt, name='dispatch')
#path('resume/list/<int:pk>/', views.GetResume, name="get_resume"),
def GetResume(request, pk):
    resume_item = get_object_or_404(Resume, id=pk)
    print("***")
    # TODO: get only what you need
    #print(resume_item)

    result = {
        'author_name': resume_item.author.username,
        'author_image': resume_item.author.profile.image.url,
        'resume_created_at': resume_item.created_at,
        'resume_filename': resume_item.filename,
        'resume_resumefile_url': resume_item.resume_file.url,
        'resume_text': resume_item.text }

    #print(result)
    return JsonResponse(result)



'''@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    # get a post HTTP request - create a new fav entry - and response 200.
    def post(self, request, pk):
        adQuery = get_object_or_404(Ad, id=pk)
        fav, created = Fav.objects.get_or_create(user=request.user, ad=adQuery)
        try:
            fav.save()
        except IntegrityError as e:
            print("Error: ", e)

        return HttpResponse()
'''


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
