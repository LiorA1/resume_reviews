from selenium.webdriver.common.by import By
from POM.base_locator import BaseLocator


class ResumeListPageLocators(BaseLocator):
    """
    A Class for ResumeList Page locators.
    All ResumeList Page Locators should come here.
    """

    LINK_LOGIN = (By.XPATH, "//a[@class='nav-item nav-link'][1]")
    SUBMIT_BUTTON = (By.ID, "submit")


class LoginPageLocators(BaseLocator):
    """
    A Class for Login Page locators.
    All Login Page Locators should come here.
    """

    form_login = (By.ID, "loginForm")
    input_username = (By.ID, "id_username")
    input_password = (By.ID, "id_password")
    button_submit = (By.ID, "submit")
    link_password_recovery = (By.XPATH, "//form[@id='loginForm']/div[@class='form-group']/small[@class='text-muted ml-2']/a")
    link_sign_up = (By.LINK_TEXT, "Sign Up")


class RegisterPageLocators(BaseLocator):
    """
    A Class for Register Page locators.
    All Register Page Locators should come here.
    """

    input_username = (By.XPATH, "//input[@id='id_username']")
    input_email = (By.XPATH, "//input[@id='id_email']")
    input_password1 = (By.XPATH, "//input[@id='id_password1']")
    input_password2 = (By.XPATH, "//input[@id='id_password2']")
    button_submit = (By.ID, "submit")
    link_sign_in = (By.LINK_TEXT, "Sign in")
