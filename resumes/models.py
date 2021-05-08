from django.db import models
from django.utils import timezone
from django.conf import settings
import os

# Create your models here.

class Resume(models.Model):

    resume_file = models.FileField(upload_to='uploads/resumes/')
    text = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def filename(self):
        return os.path.basename(self.resume_file.name)

    def __str__(self):
        return f'{self.resume_file.name} File'


class Review(models.Model):

    CHOICES = [(i, i) for i in range(11)]
    grade = models.IntegerField(choices=CHOICES)

    text = models.TextField(default="")

    #TODO: 
    #Read: https://docs.djangoproject.com/en/3.2/ref/models/fields/#datefield
    #created_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #TODO: Connect to Resume Model
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} review for {self.resume.filename} Resume'

    

    


