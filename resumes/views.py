from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'resumes/home.html')


from resumes.models import Resume
from resumes.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class ResumeListView(OwnerListView):
    model = Resume
    # By convention:
    # template_name = "myarts/<modelName>_list.html"


class ResumeDetailView(OwnerDetailView):
    model = Resume
    # By convention:
    # template_name = "myarts/<modelName>_detail.html"

class ResumeCreateView(OwnerCreateView):
    model = Resume
    fields = ['title', 'text']
    # By convention:
    # template_name = "myarts/<modelName>_form.html"
    #success_url = reverse_lazy(f'{app_name}:all')


class ResumeUpdateView(OwnerUpdateView):
    model = Resume
    fields = ['title', 'text']
    # By convention:
    # template_name = "myarts/<modelName>_form.html"


class ResumeDeleteView(OwnerDeleteView):
    model = Resume
    # By convention:
    # template_name = "myarts/<modelName>_confirm_delete.html"
