import unittest
from django.urls.base import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model


@unittest.skip("selenium")
class UITest(LiveServerTestCase):  # pragma: no cover
    host = 'app'  # Docker

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # cls.DRIVER_PATH = "C:\\chromedriver.exe"
        # cls.driver = webdriver.Chrome(cls.DRIVER_PATH)
        # Docker
        cls.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME)

        cls.driver.implicitly_wait(15)
        cls.driver.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        super().tearDownClass()

    def testresumespage(self):
        self.driver.get(f'{self.live_server_url}/resumes/list')
        assert "Django Site" in self.driver.title

    def test_register_page(self):
        register_url = reverse('accounts:register')
        self.driver.get(f'{self.live_server_url}{register_url}')
        assert "Django Site" in self.driver.title

    def create_default_user(self):
        self.data_of_user = {
            'username': 'test_ui',
            'password': 'dsfdsf4543543hgjh',
            'email': 'test@test.com',
        }
        self.user = get_user_model().objects.create_user(**self.data_of_user)

    def test_login_page(self):
        self.create_default_user()

        self.driver.get(f'{self.live_server_url}/accounts/login/')
        # button = self.driver.find_element_by_xpath("/html/body/main/")
        button = self.driver.find_element_by_xpath("//button[@id='submit']")
        user_name = self.driver.find_element_by_name('username')  # 'id_username'
        # print("**", self.data_of_user['username'])
        user_name.send_keys(self.data_of_user['username'])
        user_password = self.driver.find_element_by_name('password')  # 'id_password'
        user_password.send_keys(self.data_of_user['password'])
        button.click()
        # submit = self.driver.find_element_by_class_name("btn-outline-info")
        # submit.click()

        try:
            wait_for = WebDriverWait(self.driver, 30)
            res = wait_for.until(EC.url_changes(reverse('accounts:profile')))

        except Exception as e:
            print(f'UITest:Exception:{e}')
            self.driver.quit()

        profile_url = self.live_server_url + reverse('accounts:profile')
        self.assertEquals(self.driver.current_url, profile_url)

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
