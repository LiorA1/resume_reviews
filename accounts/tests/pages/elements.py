from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ElementByName(object):
    """
    A Class that interact with element which found by name.
    Override This class with self.locator defined, which is the name of the wanted element.
    """

    def __set__(self, object, value):
        """Sets the element text value"""

        driver = object.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_name(self.locator)
        )
        # wait_for.until(EC.presence_of_element_located(By.NAME, self.locator))

        driver.find_element_by_name(self.locator).clear()

    def __get__(self, obj, owner):
        """Gets the Text of the specified object"""
        driver = obj.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_name(self.locator)
        )

        element = driver.find_element_by_name(self.locator)

        return element.get_attribute("value")


class ElementByXPath(object):
    """
    A Class that interact with element which found by its XPATH.
    Override This class with self.locator defined, which is the XPATH of the wanted element.
    """

    def __set__(self, object, value):
        """Sets the element text value"""

        driver = object.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_xpath(self.locator)
        )
        # wait_for.until(EC.presence_of_element_located(By.XPATH, self.locator))

        driver.find_element_by_xpath(self.locator).clear()

    def __get__(self, obj, owner):
        """Gets the Text of the specified object"""
        driver = obj.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_xpath(self.locator)
        )

        element = driver.find_element_by_xpath(self.locator)

        return element.get_attribute("value")


class ElementByID(object):
    """
    A Class that interact with element which found by its ID.
    Override This class with self.locator defined, which is the ID of the wanted element.
    """

    def __set__(self, object, value):
        """Sets the element text value"""

        driver = object.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_id(self.locator)
        )
        # wait_for.until(EC.presence_of_element_located(By.XPATH, self.locator))

        driver.find_element_by_id(self.locator).clear()

    def __get__(self, obj, owner):
        """Gets the Text of the specified object"""
        driver = obj.driver
        wait_for = WebDriverWait(driver, 100)

        wait_for.until(
            lambda driver: driver.find_element_by_id(self.locator)
        )

        element = driver.find_element_by_id(self.locator)

        return element.get_attribute("value")

# ! It is required to define a class for each element type ? (buttonByName, buttonByID, etc..)
# - How To define for a button ? (there is only click ..)
