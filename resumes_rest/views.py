from django.shortcuts import render
from rest_framework import viewsets, permissions
from resumes.models import Resume, Review
from .serializers import ResumeSerializer, ReviewSerializer

# Create your views here.
from .permissions import IsAuthorOrReadOnly

class ResumeViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for Resumes
    """

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        #super(ResumeViewSet, self).perform_create(serializer)
        print("self.request.user: ", self.request.user)
        #serializer.author=self.request.user
        serializer.save(author=self.request.user)

    #def update(self, request, *args, **kwargs):




class ReviewViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for Reviews
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]