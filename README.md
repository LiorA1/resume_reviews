# resume_reviews
Resume reviews site with a Blog section.

## Introduction -
The project contains:
1. Two main CRUD operations implemented by Django.
2. One REST API implemented using DRF (see below).
3. Four Apps, including accounts App that shadows Django accounts App.
4. Multiple settings/views/models files/modules.
5. Caching.
6. N+1 Problems solutions.
7. Tests for all the Apps. (Coverage shows 96% code coverage)

The development of the project was using docker containers (docker-compose), and DJDT was integrated.
AWS S3 was used for storage.

## Further Deatails -
### Caching using memcached-
Caching using memcached was used in two ways: per-view and low level.  
Per View Caching in:
1. resumes.views.ResumeListView (in the urls module)  

Low Level was used in:  
1. resumes.views.resume_views.UserResumeListView


### N+1 Problem solved in:
1. resumes.views.resume_views.UserResumeListView (used prefetch_related)
2. resumes.views.resume_views.ResumeListView (used prefetch_related)


### DJDT -
The Django Debug Toolbar was used, as seen in the settings.development and project.urls modules.


### DRF -
The Django-REST-Framework was used as a REST API for the resumes App, as one can see in the *resumes_rest* App.
Custom Permission class as been applied for Object-level permission functionality.

### Accounts App
Used to shadow and enlarge the django default accounts App.
CustomUser is shown in the Admin interface and have registration/login/password recovery system integrated.

### Testing
Each App contains its own tests, using django.test.client and RequestFactory.
There are tests with files uploading.

### Docker
Docker was used as local development (docker-compose) environment.

### AWS
AWS S3, was used for the users images and resumes files storage.
