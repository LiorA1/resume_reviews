from selenium.webdriver.common.by import By
from POM.base_locator import BaseLocator


class ResumeListPageLocators(BaseLocator):
    """
    A Class for ResumeList Page locators.
    All ResumeList Page Locators should come here.
    """

    LINK_HOME = (By.LINK_TEXT, "Home")
    LINK_RESUMES = (By.LINK_TEXT, "Resumes")
    LINK_BLOG = (By.LINK_TEXT, "Blog")
    LINK_ABOUT = (By.LINK_TEXT, "About")

    LINK_LOGIN = (By.XPATH, "//a[@class='nav-item nav-link'][1]")
    LINK_REGISTER = (By.XPATH, "//a[@class='nav-item nav-link'][2]")

    CARD_GROUP = (By.CLASS_NAME, "cardgroup")

    FORM_SEARCH = (By.ID, "FormSearch")

    SUBMIT_BUTTON = (By.ID, "submit")


class ResumeCreatePageLocators(BaseLocator):
    """
    A Class that associates with the ResumeCreate Page Locators.
    """

    FORM_CREATE = (By.TAG_NAME, "form")

    INPUT_FILE = (By.ID, "id_resume_file")
    INPUT_TEXT = (By.ID, "id_text")
    SELECT_TAGS = (By.XPATH, "//select[@id='id_tags']")

    INPUT_SUBMIT = (By.XPATH, "//form/input[2]")
