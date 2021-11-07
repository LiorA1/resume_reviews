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

    CARD_GROUP = (By.CLASS_NAME, "cardgroup")

    FORM_SEARCH = (By.ID, "FormSearch")
    SEARCH_BUTTON = (By.XPATH, "//form[@id='FormSearch']/button")


class ResumeListPageLoggedLocators(ResumeListPageLocators):

    CREATE = (By.ID, "navbarDropdown_create")
    CREATE_RESUME = (By.LINK_TEXT, "Create Resume")
    CREATE_POST = (By.LINK_TEXT, "Create Post")

    LINK_PROFILE = (By.LINK_TEXT, "Profile")
    LINK_LOGOUT = (By.LINK_TEXT, "Logout")


class ResumeListPageLogoutLocators(ResumeListPageLocators):
    """Locators for Logout state"""

    # displayed only if not loginned
    LINK_LOGIN = (By.XPATH, "//a[@class='nav-item nav-link'][1]")
    LINK_REGISTER = (By.XPATH, "//a[@class='nav-item nav-link'][2]")


class ResumeCreatePageLocators(BaseLocator):
    """
    A Class that associates with the ResumeCreate Page Locators.
    """

    FORM_CREATE = (By.ID, "create_resume_form")

    INPUT_FILE = (By.ID, "id_resume_file")
    INPUT_TEXT = (By.ID, "id_text")
    SELECT_TAGS = (By.XPATH, "//select[@id='id_tags']")

    INPUT_SUBMIT = (By.XPATH, "//form/input[2]")


class ResumeDetailPageLocators(BaseLocator):

    CARD_HEADER = (By.CLASS_NAME, "card-header")
    CARD_BODY = (By.CLASS_NAME, "card-body")
    CARD_FOOTER = (By.CLASS_NAME, "card-footer")

    DIV_REVIEWS = (By.ID, "div_reviews")


class ResumeDetailPageLoggedLocators(ResumeDetailPageLocators):

    LINK_UPDATE_RESUME = (By.LINK_TEXT, "Update Resume")
    LINK_DELETE_RESUME = (By.LINK_TEXT, "Delete Resume")
