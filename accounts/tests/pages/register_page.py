from time import sleep
from django.urls.base import reverse
from accounts.tests.pages.locators import RegisterPageLocators
from POM.base_page import BasePage, WebDriverWait, EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class RegisterPage(BasePage):  # pragma: no cover
    """Register Page Action methods class"""

    def __init__(self, i_url: str, i_driver):
        super().__init__(i_url=i_url, i_driver=i_driver)
        self._successful_redirect_url = reverse('login')
        # I define here the driver for the auto-complete.
        #self.DRIVER_PATH = "C:\\chromedriver.exe"
        #self.driver = webdriver.Chrome(self.DRIVER_PATH)

    def check_for_locators(self):
        """
        Checks the existness of all locators from the RegisterPageLocators locator.
        Return:
            If all the locators exists - True.
            Otherwise - False.
        """
        return super(RegisterPage, self).check_for_locators(RegisterPageLocators)

    def _click_signup_button(self):
        """Click the registration button"""
        button = self.driver.find_element(*RegisterPageLocators.button_submit)

        # Because scroll requires to find the button
        try:
            ActionChains(self.driver).move_to_element(button).perform()
            wait_for = WebDriverWait(self.driver, 15)
            res = wait_for.until(EC.element_to_be_clickable(*RegisterPageLocators.button_submit))

            if res:
                button.click()
            else:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
        except Exception as e:
            print(f'_click_signup_button:Exception:{e}')
            self.driver.execute_script("arguments[0].click();", button)

    def submit_register_form(self, i_username: str, i_email: str, i_password: str):
        """Submit the registration form with the given parameters."""
        res = False

        try:
            username_ele = self.driver.find_element(
                *RegisterPageLocators.input_username)
            email_ele = self.driver.find_element(
                *RegisterPageLocators.input_email)
            pass1_ele = self.driver.find_element(
                *RegisterPageLocators.input_password1)
            pass2_ele = self.driver.find_element(
                *RegisterPageLocators.input_password2)

            username_ele.send_keys(i_username)
            email_ele.send_keys(i_email)
            pass1_ele.send_keys(i_password)
            pass2_ele.send_keys(i_password)
            self._click_signup_button()
            res = True
        except Exception as e:
            print(f'submit_register_form:Exception:{e}')
        finally:
            return res

    def is_redirected_correctly(self):
        """
        Check if the current url is the url after successful registration.
        (login url)\n
        Return:
            If the url is the correct one - True.
            Otherwise - False
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

    def is_url_register(self, i_register_url: str):
        return self.url == i_register_url
