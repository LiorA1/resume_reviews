from accounts.models import CustomUser
from accounts.tests.pages.login_page import LoginPage
from resumes.models import Resume
from resumes.tests.pages.resumes_list_page import ListPage
from resumes.tests.pages.resume_create_page import CreateResumePage
from resumes.tests.pages.resume_detail_page import DetailResumePage
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
import os
from unittest import skipIf
from django.test.utils import override_settings
from django.urls.base import reverse
from django.test.client import Client


CACHES_SELENIUM = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


class UITest(LiveServerTestCase):  # pragma: no cover

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        DOCKER_ENV = os.environ.get('DOCKER_ENV', '') == 'True'

        if DOCKER_ENV:
            # DOCKER
            pass
        else:
            cls.DRIVER_PATH = "C:\\chromedriver.exe"
            cls.driver = webdriver.Chrome(cls.DRIVER_PATH)

        # Docker
        #cls.driver = webdriver.Remote(
        #    command_executor="http://selenium:4444/wd/hub",
        #    desired_capabilities=DesiredCapabilities.CHROME)

        cls.driver.implicitly_wait(15)
        cls.driver.set_page_load_timeout(30)
    
    # TODO: try to move the driver initialization to setUp.

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        super().tearDownClass()

    def set_user_data(self, i_username: str = "test_ui", i_email: str = "test@test.com", i_pass: str = "tkdalf543x"):
        self.data_of_user = {
            'username': i_username,
            'password': i_pass,
            'email': i_email,
        }

    def create_user_instance(self, i_username: str = "test_ui", i_pass: str = "tkdalf543x", i_email: str = "test@test.com"):
        self.data_of_user = {
            'username': i_username,
            'password': i_pass,
            'email': i_email,
        }
        self.user = get_user_model().objects.create_user(**self.data_of_user)


@skipIf(os.environ.get('DOCKER_ENV', '') == 'True', "selenium")
class ResumeListUITest(UITest):  # pragma: no cover

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        resumes_list_path = reverse('resumes:resume_list')
        cls.resumes_list_url = f'{cls.live_server_url}{resumes_list_path}'

        cls._ResumesListPage = ListPage(cls.resumes_list_url, cls.driver)

    # !Override the caches, before test with selenium
    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resumes_list_page_reachable(self):
        self.driver.get(self.resumes_list_url)

        self.assertEqual("Django Site", self.driver.title)

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_card_group_presence(self):
        list_resumes = self._ResumesListPage
        list_resumes.load_page()

        res_locators = list_resumes.check_for_locators_logout()
        self.assertTrue(res_locators)

        # Check if empty
        self.assertTrue(list_resumes.is_empty())

        self.assertTrue(list_resumes.is_current_url(self.resumes_list_url))

        # python manage.py test resumes.tests.test_selenium


@skipIf(os.environ.get('DOCKER_ENV', '') == 'True', "selenium")
class ResumeCreateUITest(UITest):  # pragma: no cover

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        resume_create_path = reverse('resumes:resume_create')
        cls.resume_create_url = f'{cls.live_server_url}{resume_create_path}'

        cls._ResumeCreatePage = CreateResumePage(cls.resume_create_url, cls.driver)

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_create_page_loggedout(self):
        """Test the appearance of the create page as an AnonymousUser"""
        resume_create = self._ResumeCreatePage
        resume_create.load_page()

        res_locators = resume_create.check_for_locators_logout()
        self.assertTrue(res_locators == 0)
        self.assertFalse(resume_create.is_current_url(self.resume_create_url))

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_create_page_loggedin(self):
        """Test the appearance of the create page as CustomUser"""
        resume_create = self._ResumeCreatePage
        resume_create.load_page()

        self.create_user_instance()
        login_page = LoginPage(self.live_server_url, self.driver)
        res_locators = login_page.check_for_locators()
        self.assertTrue(res_locators)

        res_login = login_page.submit_login_form(self.data_of_user['username'], self.data_of_user['password'])
        self.assertTrue(res_login)

        #
        res_locators = resume_create.check_for_locators_logged()
        self.assertTrue(res_locators == 1.0)

        self.assertTrue(resume_create.is_current_url(self.resume_create_url))


@skipIf(os.environ.get('DOCKER_ENV', '') == 'True', "selenium")
class ResumeDetailUITest(UITest):  # pragma: no cover

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        FOLDER_NAME = 'data'
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        cls.TEST_DATA_DIR = os.path.join(TEST_DIR, FOLDER_NAME)

        resume_id = 1
        resume_detail_path = reverse('resumes:resume_detail', args={resume_id})
        cls.resume_detail_url = f'{cls.live_server_url}{resume_detail_path}'

        #cls._ResumeDetailPage = DetailResumePage(cls.resume_detail_url, cls.driver)

    def setUp(self) -> None:
        self._ResumeDetailPage = DetailResumePage(self.resume_detail_url, self.driver)
        self.create_user_instance()
        return super().setUp()

    def tearDown(self) -> None:

        self.resume = None
        self.user = None
        self._ResumeDetailPage = None

        return super().tearDown()

    def create_resume_instance(self, i_file_path: str, i_text: str, i_author: CustomUser):

        self.resume = Resume(resume_file=i_file_path, text=i_text, author=i_author)

        return self.resume.save()

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_detail_page_404(self):
        """
        Test the appearance of the non exists detail page as an AnonymousUser
        """
        resume_detail = self._ResumeDetailPage
        resume_detail.load_page()

        # gets 404, because no instance exists
        res_locators = resume_detail.check_for_locators()
        self.assertFalse(res_locators)

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_detail_page_loggedout(self):
        """
        Test the appearance of the detail page as an AnonymousUser
        """
        #

        #
        # Resume Creation
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')
        self.create_resume_instance(pdf_file_path, "text", self.user)
        self.assertTrue(Resume.objects.count() == 1)

        # all the locators
        resume_detail = self._ResumeDetailPage
        resume_detail.load_page()

        res_locators = resume_detail.check_for_locators()
        self.assertTrue(res_locators)  # ?

        # TODO: Each time that uploads a resume - need to delete it !

        # Something is wrong !!
        # tried to create Resume while NOT loggedin ?

        # Alone it will run.
        # With the class it will not..

        # 1. Check AWS settings..

        # Problems:
        # 1. Dont saves to AWS
        # 2. Alone it is working, Whole class is not.

        # BUG:
        # "alone ok, whole fail" Bug. attributes problems.

        # python manage.py test resumes.tests.test_selenium.ResumeDetailUITest.test_resume_detail_page_loggedout

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_detail_page_loggedin(self):
        """
        Test the appearance of the detail page as CustomUser
        """

        # Log in
        #self.create_user_instance()
        login_path = reverse('login')
        login_url = f'{self.live_server_url}{login_path}'

        # Log in
        login_page = LoginPage(login_url, self.driver)
        login_page.load_page()
        res_locators = login_page.check_for_locators()
        self.assertTrue(res_locators)
        res_login = login_page.submit_login_form(self.data_of_user['username'], self.data_of_user['password'])
        self.assertTrue(res_login)

        #
        # Resume Creation
        pdf_file_path = os.path.join(self.TEST_DATA_DIR, 'resume_sample.pdf')
        self.create_resume_instance(pdf_file_path, "text", self.user)
        self.assertTrue(Resume.objects.count() == 1)

        # return to detailview while logged in
        resume_detail = self._ResumeDetailPage
        resume_detail.load_page()

        #
        res_locators = resume_detail.check_for_locators_logged()
        self.assertTrue(res_locators == 1.0)

        self.assertTrue(resume_detail.is_current_url(self.resume_detail_url))

        # python manage.py test resumes.tests.test_selenium.ResumeDetailUITest.test_resume_detail_page_loggedin
