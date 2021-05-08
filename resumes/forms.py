
# Create a Resume Form
# Create a Review Form


from django import forms
from resumes.models import Resume, Review

class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ['resume_file', 'text']
        #author will be tied in the create view


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['grade', 'text']
        #author,resume will be tied in the create view