from resumes.tests.pages.resumes_list_page import ListPage
from resumes.tests.pages.create_resume_page import CreateResumePage
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
import os
from unittest import skipIf
from django.test.utils import override_settings
from django.urls.base import reverse


CACHES_SELENIUM = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


class UITest(LiveServerTestCase):

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

        res_locators = list_resumes.check_for_locators()
        self.assertTrue(res_locators)

        # Check if empty
        self.assertTrue(list_resumes.is_empty())

        self.assertTrue(list_resumes.is_current_url(self.resumes_list_url))

        # python manage.py test resumes.tests.test_selenium


@skipIf(os.environ.get('DOCKER_ENV', '') == 'True', "selenium")
class ResumeCreateUITest(UITest): # pragma: no cover

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        resume_create_path = reverse('resumes:resume_create')
        cls.resume_create_url = f'{cls.live_server_url}{resume_create_path}'

        cls._ResumeCreatePage = CreateResumePage(cls.resume_create_url, cls.driver)

    @override_settings(DEBUG=True, CACHES=CACHES_SELENIUM)
    def test_resume_create_page(self):
        resume_create = self._ResumeCreatePage
        resume_create.load_page()

        res_locators = resume_create.check_for_locators()
        self.assertTrue(res_locators < 0.5)

        self.assertFalse(resume_create.is_current_url(self.resume_create_url))
