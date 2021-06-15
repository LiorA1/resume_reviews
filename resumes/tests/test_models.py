from django.test import TestCase
from ..models import Resume, Review, Tag
from accounts.models import CustomUser

from unittest import mock
from django.core.files import File

class ResumeModelTestCase(TestCase):

    def setUp(self) -> None:
        # Create a CustomUser
        self.user_a = CustomUser(username="la", email='la@test.co.il')
        self.password = 'tilt5pivot2'
        self.user_a.set_password(self.password)
        self.user_a.save()
        # Create a Resume
        ## Create a Mock
        self.resume_pdf_mock = mock.MagicMock(spec=File)
        self.resume_pdf_mock.name = "test.pdf"
        ## Create a Resume
        self.text = "test text"
        self.resume_model = Resume(resume_file=self.resume_pdf_mock, text=self.text, author=self.user_a)
        


        return super().setUp()

    def test_resume_attributes(self):
        
        #print(self.resume_model.__dict__)
        self.assertEqual(str(self.resume_model), f'{self.resume_pdf_mock.name} File')
        self.assertEqual(self.resume_model.filename, f'{self.resume_pdf_mock.name}')
        self.assertEqual(self.resume_model.text, f'{self.text}')

    
    def test_review_attributes(self):
        self.grade = 1
        self.review_model = Review(grade=self.grade, text=self.text, resume=self.resume_model, author=self.user_a)
        #self.review_model.save(commit=False)
        self.assertEqual(str(self.review_model), f'{self.review_model.author} review for {self.review_model.resume.filename} Resume')
        self.assertEqual(self.review_model.text, self.text)


    def test_tag_attributes(self):
        self.tag_name="tag"
        self.tag_model = Tag(name=self.tag_name)
        self.assertEqual(str(self.tag_model), f'{self.tag_name}')
        count=Tag.objects.count()
        self.assertEqual(repr(self.tag_model), f'{self.tag_name} (id:{self.tag_model.id})')
