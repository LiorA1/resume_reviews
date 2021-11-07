from .locators import ResumeDetailPageLocators, ResumeDetailPageLoggedLocators
from selenium import webdriver
from POM.base_page import BasePage, WebDriverWait, EC


class DetailResumePage(BasePage):  # pragma: no cover
    """Resume Detail View"""

    def __init__(self, i_url: str = None, i_driver=None):
        super().__init__(i_url=i_url, i_driver=i_driver)

        #self.DRIVER_PATH = "C:\\chromedriver.exe"
        #self.driver = webdriver.Chrome(self.DRIVER_PATH)

    def check_for_locators(self):
        return super(DetailResumePage, self).check_for_locators(ResumeDetailPageLocators)

    def check_for_locators_logged(self):
        return super(DetailResumePage, self).check_for_locators(ResumeDetailPageLoggedLocators)