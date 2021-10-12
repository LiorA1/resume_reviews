
from .locators import ResumeListPageLocators
from selenium import webdriver
from POM.base_page import BasePage, WebDriverWait, EC


class ListPage(BasePage):  # pragma: no cover
    """ListPage Action methods class"""

    def __init__(self, i_url: str, i_driver):
        super().__init__(i_url=i_url, i_driver=i_driver)

        #self.DRIVER_PATH = "C:\\chromedriver.exe"
        #self.driver = webdriver.Chrome(self.DRIVER_PATH)

    def check_for_locators(self):
        return super(ListPage, self).check_for_locators(ResumeListPageLocators)

    def is_empty(self):
        """
        Checks if the resume list is empty.
        True - if empty. False - Otherwise.
        """
        res = False
        cardgroup_e = self.driver.find_element(*ResumeListPageLocators.CARD_GROUP)

        all_childern = cardgroup_e.find_elements_by_class_name("card")

        if len(all_childern) == 1:
            if all_childern[0].text == "No Resumes was found":
                res = True

        return res

        # python manage.py test resumes.tests.test_selenium
