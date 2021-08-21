from accounts.models import CustomUser
import re
from typing import List
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.functions.text import Lower
from django.db.models.query_utils import Q
from django.urls.base import reverse
from django.utils import timezone
from django.conf import settings
import os
from django.core.cache import cache

# Create your models here.


class ResumeQuerySet(models.QuerySet):
    # Make a query method, that return any resume that belong any Tag from the given list

    def filter_by_tags(self, tags_id: List):
        """Filter by a given list of Tags id's"""
        return self.filter(tags__in=tags_id)

    # add a field of how many tags has any resume
    def score_tags(self):
        """
        Add a field 'score', which summerize how many tags each resume has.
        """
        return self.annotate(score=Count('tags'))

    # add a field of how many tags has any resume (from a given tags list)
    def score_tags_by_list(self, tags_id: List):
        """
        Add a field 'score', which summerize how many tags from the tags_id list each resume has.
        """
        Q_query = Q(tags__in=tags_id)
        return self.annotate(score=Count('tags', filter=Q_query))

    def filter_by_user_orderby_fetch(self, io_customUser: CustomUser, order_fields: List, fetch_fields: List):
        '''
        Filter Resumes by given "CustomUser", order by "order_fields" and fetching the "fetch_fields"
        Saves the Query in the cache for 300 seconds
        Return the wanted QuerySet.
        '''
        # get the resumes QuerySet of the user, Using low level caching
        user_resumes_key = str(io_customUser.username + "_resumes")
        resumes_queryset = cache.get(user_resumes_key)
        if resumes_queryset is None:
            resumes_queryset = self.filter(author=io_customUser).order_by(*order_fields).prefetch_related(*fetch_fields)
            cache.set(user_resumes_key, resumes_queryset, timeout=300)

        return resumes_queryset


class Resume(models.Model):
    """Resume Model"""

    resume_file = models.FileField(upload_to='uploads/resumes/')
    text = models.TextField(default="")
    tags = models.ManyToManyField('Tag', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = ResumeQuerySet.as_manager()

    @property
    def filename(self):
        return os.path.basename(self.resume_file.name)

    def __str__(self):
        return f'{self.resume_file.name} File'

    def get_absolute_url(self):
        return reverse('resumes:resume_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    """Review Model"""

    CHOICES = [(i, i) for i in range(11)]
    grade = models.IntegerField(choices=CHOICES)

    text = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} review for {self.resume.filename} Resume'


class TagQuerySet(models.QuerySet):

    def lower_cased_name(self):
        '''Will Add a 'lower_name' field'''
        return self.annotate(lower_name=Lower('name'))

    def filter_by_lower_name(self, lower_names: List):
        return self.filter(lower_name__in=lower_names)

    def tags_id_from_str(self, searchTerm: str):
        '''Will return all tags id's that their names is in the given string'''
        # Find all existing tags
        exists_tags = self.lower_cased_name()

        # # Cache It (Get the e_t_l_n from the cached if exists there)
        e_t_l_n_key = str("resumes_tags_cache")
        existing_tags_lower_name = cache.get(e_t_l_n_key)
        if existing_tags_lower_name is None:
            # Find all existing tags names (in lower case)
            existing_tags_lower_name = exists_tags.values_list('lower_name', flat=True)
            cache.set(e_t_l_n_key, existing_tags_lower_name, timeout=60*60*24)

        # Build a REGEX to help find the tags names that is in the search string
        look_for = "|".join(f'\\b{p}\\b' for p in existing_tags_lower_name)

        # find all expressions from the search string
        required_tags_lower_name = re.findall(look_for, searchTerm.lower())

        # Find the Tags instances themselves
        tags_required = exists_tags.filter_by_lower_name(required_tags_lower_name).values_list('id', flat=True)

        return tags_required


class Tag(models.Model):
    """Tag Model (been added after the initial db design)"""
    name = models.CharField(max_length=25)

    objects = TagQuerySet.as_manager()

    def __repr__(self):
        return f'{self.name} (id:{self.pk})'

    def __str__(self):
        return f'{self.name}'
