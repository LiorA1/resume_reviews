
from .elements import ElementByName
from django.urls.base import reverse
from selenium import webdriver
from .locators import LoginPageLocators
from POM.base_page import BasePage, WebDriverWait, EC


class LoginPage(BasePage):  # pragma: no cover
    """Login Page Action methods class"""
    # https://github.com/paulbodean88/automation-design-patterns/blob/master/src/page_object_pattern/home_page.py

    def __init__(self, i_url: str, i_driver):
        super().__init__(i_url=i_url, i_driver=i_driver)
        self._successful_redirect_url = reverse('accounts:profile')
        # self.link_login = LinkLoginElement()
        # I define here the driver for the auto-complete.
        #self.DRIVER_PATH = "C:\\chromedriver.exe"
        #self.driver = webdriver.Chrome(self.DRIVER_PATH)

    def check_for_locators(self):
        """
        Checks the existness of all locators from the LoginPageLocators locator.
        Return:
            If all the locators exists - True.
            Otherwise - False.
        """
        return super(LoginPage, self).check_for_locators(LoginPageLocators)

    def _click_login_link(self):
        """Click the login button"""

        element = self.driver.find_element(*LoginPageLocators.button_submit)
        element.click()

    def submit_login_form(self, i_username: str, i_password: str):
        """Submit the login form with the given parameters."""
        res = False

        try:
            username_element = self.driver.find_element(
                *LoginPageLocators.input_username)
            password_element = self.driver.find_element(
                *LoginPageLocators.input_password)

            username_element.send_keys(i_username)
            password_element.send_keys(i_password)
            self._click_login_link()
            res = True
        except Exception as e:
            print(f'submit_login_form:Exception:{e}')
        finally:
            return res

    def is_redirected_correctly(self):
        """
        Checks if after the login the user was redirect to the correct url.
        Return:
            True, If the url is redirected to the correct one, in the frame time.
            False, Otherwise.
        """
        res = False

        try:
            redirect_url = self._successful_redirect_url
            wait_for = WebDriverWait(self.driver, 30)
            res = wait_for.until(EC.url_matches(redirect_url))
        except Exception as e:
            print(f'is_redirected_correctly:\nException:{e}.')
            print(f'Current url is: {self.driver.current_url}.')
        finally:
            return res

    def is_url_login(self, i_login_url: str):
        return self.url == i_login_url
