from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.conf import settings
import os

# Create your models here.

"""Resume Model"""
class Resume(models.Model):

    resume_file = models.FileField(upload_to='uploads/resumes/')
    text = models.TextField(default="")
    tags = models.ManyToManyField('Tag', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def filename(self):
        return os.path.basename(self.resume_file.name)

    def __str__(self):
        return f'{self.resume_file.name} File'

    def get_absolute_url(self):
        return reverse('resumes:resume_detail', kwargs = {'pk': self.pk})



"""Review Model"""
class Review(models.Model):

    CHOICES = [(i, i) for i in range(11)]
    grade = models.IntegerField(choices=CHOICES)

    text = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} review for {self.resume.filename} Resume'

    

    


"""Tag Model (been added after the initial db design)"""
class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __repr__(self):
        return f'{self.name} (id:{self.pk})'

    def __str__(self):
        return f'{self.name}'