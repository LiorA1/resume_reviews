
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from accounts.tests.pages.locators import BaseLocator


class BasePage(object):
    """A Base Page Action methods class."""

    def __init__(self, i_url: str = None, i_driver=None):
        self.driver = i_driver
        self.url = i_url

    def load_page(self):
        """Loads the url, given in self.url."""
        return self.driver.get(self.url)

    def is_title_matches(self, i_str: str) -> bool:
        """
        Checks the page title, for contains a given string.
        Return True If i_str is the title. False - Otherwise.
        """
        return i_str == self.driver.title

    def check_for_locators(self, locator_class: BaseLocator):
        """
        Checks the existness of all locators from the given locator in the child page call.
        BaseLocator - the parent of all Locators classes.
        Return:
            If all the locators exists - True.
            Otherwise - False.
        """
        res = False
        try:
            for (key, val) in locator_class.__dict__.items():
                if not key.startswith('_'):
                    wait_for = WebDriverWait(self.driver, 15)
                    wait_for.until(EC.presence_of_element_located(val))
            res = True
        except Exception as e:
            print(f'check_for_locators: {e}.\nKey: {key}')
        finally:
            return res
