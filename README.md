# resume_reviews
Resume reviews site with a Blog section.

## Introduction -
The project contains:
1. Two main CRUD operations implemented by Django.
2. One REST API implemented using DRF (see below).
3. Four Apps, including accounts App that shadows Django accounts App.
4. Multiple settings/views/models files/modules.
5. [Caching.](/resume_project/settings/development.py#L24)
6. N+1 Problems solutions.
7. Tests using TestCase (python.unittest)for all the Apps. (Coverage shows 96% code coverage)
8. Selenium Tests for Accounts App, using Page Object Model & Locators Design.

The development of the project was using docker containers (docker-compose), and DJDT was integrated.
AWS S3 was used for storage.

## Further Deatails -
### Caching using memcached-
Caching using memcached was used in two ways: per-view and low level.
All Caching is defined in two types of modules:
per view is done in the urls module, for better maintainability and readability.
low level caching is concentrated in the models modules, which interacts directly with the Database and allows flexability between the DB and the caching framework, in a visiable and coherent manner.

Per View Caching in:
1. [resumes.urls](/resumes/urls.py#L30) - Caching static views. ("home" view)

Low Level was used in:  
1. [resumes.models](/resumes/models.py#L39)


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
Coverage shows a 96% coverage of the project.

### Selenium Testing
Accounts App is tested using Selenium, using Page Object Model (POM) and Locators Design. Using Inheritance to develop code that is keeping the DRY principle.

### Docker
Docker was used as local development (docker-compose) environment.

### AWS
AWS S3, was used for the users images and resumes files storage.


## Additional Remarks -
1. Only approved posts will be published (Using Custom QuerySet)
2. DRF - Secondary serializer for '.update' operation. (/resumes_rest/views.py#L25)
3. Search Bar for resumes and blogs, with score calculation, where its possible.
4. Custom QuerySets & Managers in the resumes App, which abstract the logic and caches the heavy queries.