
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from resumes.models import Resume, Review, Tag


class ResumeSerializer(serializers.ModelSerializer):
    #author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    class Meta:
        model = Resume
        fields = ['id', 'resume_file', 'text', 'tags']#, 'author']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['grade', 'text', 'resume', 'author']