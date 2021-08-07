from accounts.tests.pages.register_page import RegisterPage
from time import sleep

from django.test.utils import override_settings
from accounts.tests.pages.login_page import LoginPage

from django.urls.base import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model
import unittest


@unittest.skip("selenium")
class UITest(LiveServerTestCase):  # pragma: no cover
    #host = 'app'  # Docker

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
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
        cls.driver.quit()
        super().tearDownClass()

    #@override_settings(DEBUG=True)
    # TODO: Why a cached view cant be tested ?
    def test_resumes_page(self):
        resumes_list_path = reverse('resumes:resume_list')
        resumes_list_url = f'{self.live_server_url}{resumes_list_path}'
        self.driver.get(resumes_list_url)

        try:
            wait_for = WebDriverWait(self.driver, 30)
            res = wait_for.until(EC.title_is("Django Site"))
        except Exception as e:
            print(f'UITest:Exception:{e}')
            self.driver.quit()

        self.assertEqual("Django Site", self.driver.title)

    def initialize_user_data(self, i_username: str = "test_ui", i_email: str = "test@test.com", i_pass: str = "tkdalf543x"):
        self.data_of_user = {
            'username': i_username,
            'password': i_pass,
            'email': i_email,
        }

    def test_register_page(self):
        register_path = reverse('accounts:register')
        register_url = f'{self.live_server_url}{register_path}'

        register_page = RegisterPage(register_url, self.driver)
        register_page.load_page()
        res_locators = register_page.check_for_locators()
        self.assertTrue(res_locators)

        res_title = register_page.is_title_matches("Django Site")
        self.assertTrue(res_title)

        self.initialize_user_data()

        res_register = register_page.submit_register_form(
            self.data_of_user['username'],
            self.data_of_user['email'],
            self.data_of_user['password'])
        self.assertTrue(res_register)

        res_redirect = register_page.is_redirected_correctly()
        self.assertTrue(res_redirect)

    def create_user_instance(self, i_username: str = "test_ui", i_pass: str = "tkdalf543x", i_email: str = "test@test.com"):
        self.data_of_user = {
            'username': i_username,
            'password': i_pass,
            'email': i_email,
        }
        self.user = get_user_model().objects.create_user(**self.data_of_user)

    def test_login_page(self):
        self.create_user_instance()

        login_path = reverse('login')
        login_url = f'{self.live_server_url}{login_path}'

        login_page = LoginPage(login_url, self.driver)
        login_page.load_page()
        res_locators = login_page.check_for_locators()
        self.assertTrue(res_locators)

        self.assertTrue(login_page.is_url_login(login_url))

        res_title = login_page.is_title_matches("Django Site")
        self.assertTrue(res_title)

        res_login = login_page.submit_login_form(self.data_of_user['username'], self.data_of_user['password'])
        self.assertTrue(res_login)

        res_redirect = login_page.is_redirected_correctly()
        self.assertTrue(res_redirect)




# python manage.py test accounts.tests.test_selenium


    #    try:
    #        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card")))
    #        print(len(element))
    #    except Exception as e:
    #        driver.quit()

    #   driver.back() go back
    #   driver.forward()

    #   driver.find_element(By.css)

    #   submit.send_keys(keys.RETURN)
