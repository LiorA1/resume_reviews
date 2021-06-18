from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls.base import reverse
# Create your views here.


from resumes.models import Resume, Review
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views.generic import ListView

from ..forms import ResumeForm, ReviewForm

from accounts.models import CustomUser




import time 
def home(request):
    time.sleep(5)
    return render(request, 'resumes/home.html')



"""Display all the resumes"""
class ResumeListView(OwnerListView):
    model = Resume
    ordering = ['-created_at']
    #paginate_by = 1
    # By convention:
    # template_name = "resumes/<modelName>_list.html"
    queryset = Resume.objects.prefetch_related('tags', 'author', 'author__profile')




from django.core.cache import cache

"""ListView of Resumes specific by the User"""
class UserResumeListView(ListView):
    model = Resume
    template_name = 'resumes/user_resumes.html'
    #context_object_name = 'resumes'

    def get_queryset(self):
        #start_time = time.perf_counter()

        # get the user instance (needed for lookup)
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        # get the resumes QuerySet of the user
        user_resumes_key = str(user.username + "_resumes")
        resumes_queryset = cache.get(user_resumes_key)
        if resumes_queryset is None:
            print("***insert to cache***")
            resumes_queryset = Resume.objects.filter(author=user).order_by('-id').prefetch_related('tags', 'author', 'author__profile')
            cache.set(user_resumes_key, resumes_queryset, timeout=300)
            #TODO: Caching is not apper in the djdt for some reason

        #finish_time = time.perf_counter()
        #print("UserResumeListView:get_queryset - After")
        #print(f'Finished in {finish_time-start_time} seconds')
        # The improvement is near to 50%.
        
        return resumes_queryset



""" Resume Detail Page/View with ReviewForm"""
class ResumeDetailView(OwnerDetailView):
    model = Resume
    # By convention:
    # template_name = "resumes/<modelName>_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ResumeDetailView, self).get_context_data(**kwargs)

        # Getting the Specific Resume 
        pk = self.kwargs['pk']
        resumeQuery = get_object_or_404(Resume, id=pk)

        # Get all the reviews belongs to the Resume
        reviews = Review.objects.filter(resume=resumeQuery).order_by('-updated_at')
        review_form = ReviewForm()
        context = {'resume': resumeQuery, 'reviews': reviews, 'review_form': review_form}

        return context


""" Resume Create Page/View """
class ResumeCreateView(OwnerCreateView):
    model = Resume
    #fields = ['resume_file', 'text']
    form_class = ResumeForm
    # By convention:
    # template_name = "resumes/<modelName>_form.html"
    #success_url = reverse_lazy(f'{app_name}:all')


""" Resume Update Page/View """
class ResumeUpdateView(OwnerUpdateView):
    model = Resume
    fields = ['resume_file', 'text', 'tags']
    # By convention:
    # template_name = "resumes/<modelName>_form.html"

    def get_success_url(self):
        print("ResumeUpdateView:get_success_url")
        print("pk is:", self.kwargs.get('pk'))
        return reverse('resumes:resume_detail', args=[self.kwargs.get('pk')])


""" Resume Delete Page/View """
class ResumeDeleteView(OwnerDeleteView):
    model = Resume
    # By convention:
    # template_name = "resumes/<modelName>_confirm_delete.html"











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
