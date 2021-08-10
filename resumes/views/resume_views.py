from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.db.models import Q, Count
# Create your views here.
import re
from django.db.models.functions import Lower

from resumes.models import Resume, Review, Tag
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, ParentOwnerDetailView
from django.views.generic import ListView

from ..forms import ResumeForm, ReviewForm

from accounts.models import CustomUser


import time
from django.core.cache import cache


def home(request):
    time.sleep(5)
    return render(request, 'resumes/home.html')


class ResumeListView(OwnerListView):
    """Display all the resumes"""
    model = Resume
    ordering = ['-created_at']
    # template_name = "resumes/<modelName>_list.html"
    queryset = Resume.objects.prefetch_related('tags', 'author', 'author__profile')

    def get_queryset(self):
        self.queryset = super(ResumeListView, self).get_queryset()

        # Check for searchTerm existence
        searchTerm = self.request.GET.get("search", False)
        if searchTerm:
            # Find all existing tags
            exists_tags = Tag.objects.annotate(lower_name=Lower('name'))

            # Find all existing tags names (in lower case)
            existing_tags_lower_name = exists_tags.values_list('lower_name', flat=True)

            # Build a REGEX to help find the tags names that is in the search string
            look_for = "|".join(f'\\b{p}\\b' for p in existing_tags_lower_name)

            # find all expressions from the search string
            required_tags_lower_name = re.findall(look_for, searchTerm.lower())

            # Find the Tags instances themselves
            tags_required = exists_tags.filter(lower_name__in=required_tags_lower_name).values_list('id', flat=True)

            # By now, I have all the tags the user search for
            # Lets look for the resumes associated with them

            # Query which resumes have the wanted tags, order by the match score.
            Q_query = Q(tags__in=tags_required)
            self.queryset = self.queryset.filter(tags__isnull=False).distinct().annotate(score=Count('tags', filter=Q_query)).filter(score__gt=0).order_by('-score')

        return self.queryset


class UserResumeListView(ListView):
    """ListView of Resumes specific by the User"""
    model = Resume
    template_name = 'resumes/user_resumes.html'

    def get_queryset(self):
        # start_time = time.perf_counter()

        # get the user instance (needed for lookup)
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))

        # get the resumes QuerySet of the user, Using low level caching
        user_resumes_key = str(user.username + "_resumes")
        resumes_queryset = cache.get(user_resumes_key)
        if resumes_queryset is None:
            # print("***insert to cache***")
            resumes_queryset = Resume.objects.filter(author=user).order_by('-id').prefetch_related('tags', 'author', 'author__profile')
            cache.set(user_resumes_key, resumes_queryset, timeout=300)
            # TODO: Caching is not appear in the djdt for some reason

        # finish_time = time.perf_counter()
        # print("UserResumeListView:get_queryset - After")
        # print(f'Finished in {finish_time-start_time} seconds')
        #  The improvement is near to 50%.

        return resumes_queryset


class ResumeDetailView(ParentOwnerDetailView):
    """ Resume Detail Page/View with ReviewForm"""
    model = Resume
    child_model = Review
    child_form = ReviewForm


class ResumeCreateView(OwnerCreateView):
    """ Resume Create Page/View """
    model = Resume
    # fields = ['resume_file', 'text']
    form_class = ResumeForm
    # template_name = "resumes/<modelName>_form.html"


class ResumeUpdateView(OwnerUpdateView):
    """ Resume Update Page/View """
    model = Resume
    fields = ['resume_file', 'text', 'tags']

    def get_success_url(self):
        # print("ResumeUpdateView:get_success_url")
        # print(f'pk is: {self.kwargs.get("pk")}')
        return reverse('resumes:resume_detail', args=[self.kwargs.get('pk')])


class ResumeDeleteView(OwnerDeleteView):
    """ Resume Delete Page/View """
    model = Resume
    # template_name = "resumes/<modelName>_confirm_delete.html"











#TODO Section:
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
