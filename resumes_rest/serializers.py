
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from resumes.models import Resume, Review


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['resume_file', 'text', 'author']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['grade', 'text', 'resume', 'author']