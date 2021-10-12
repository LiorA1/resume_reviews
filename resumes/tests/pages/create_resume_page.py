from .locators import ResumeCreatePageLocators
from selenium import webdriver
from POM.base_page import BasePage, WebDriverWait, EC


class CreateResumePage(BasePage):  # pragma: no cover
    """Resume Create Page"""

    def __init__(self, i_url: str, i_driver):
        super().__init__(i_url=i_url, i_driver=i_driver)

        #self.DRIVER_PATH = "C:\\chromedriver.exe"
        #self.driver = webdriver.Chrome(self.DRIVER_PATH)

    def check_for_locators(self):
        return super(CreateResumePage, self).check_for_locators(ResumeCreatePageLocators)
