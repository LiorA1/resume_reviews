"""resume_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    
    path('resumes/', include('resumes.urls')),

    path('resumes_rest/', include('resumes_rest.urls')),

    path('blog/', include('blog.urls')),

    path('about/', TemplateView.as_view(template_name="about.html"), name="site_about"),

    path('', include('accounts.urls')),

]


#https://docs.djangoproject.com/en/3.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
if settings.DEBUG:
    
    print("Debug == True")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

    if settings.DEBUG_TOOLBAR_ENABLED:
        print("DEBUG_TOOLBAR_ENABLED == True")
        import debug_toolbar
        urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))

    
    
    # Using in this way, it will be more understandable.
    # TODO: read about it more!
    # Only Add this when we in debug mode





    # TODO Highlighted as a TODO
    #- This will also be highlighted as a TODO (Prefixed with a -)
    # This will be an unhighlighted comment
    #! This is another comment
    #- and again, continued highlighting
    #* Deprecated
    #? Question