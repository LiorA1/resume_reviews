
from rest_framework import serializers
from resumes.models import Resume, Review, Tag


class ResumeSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    class Meta:
        model = Resume
        fields = ['id', 'resume_file', 'text', 'tags']


class ResumeTextSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()

    class Meta:
        model = Resume
        fields = ['id', 'resume_file', 'text', 'tags']#, 'author']
        extra_kwargs = {'id': {'required': False}, 'resume_file': {'required': False}}


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['grade', 'text', 'resume', 'author']
