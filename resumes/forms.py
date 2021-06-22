
# Create a Resume Form
# Create a Review Form


from django import forms
from resumes.models import Resume, Review

class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ['resume_file', 'text', 'tags']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['grade', 'text']