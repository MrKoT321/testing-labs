from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

PRODUCT_NAME_IN_CATALOG = "//input[@id='typeahead']"
PRODUCT_NAME_IN_PRODUCT_PAGE = "//h3[contains(text(), '{}')]"


class Catalog:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def search_product(self, text):
        try:
            self._type_in_search_input(text)
            self._submit_search_with_enter()
        except Exception as e:
            return e

    def find_product(self, product_name):
        try:
            xpath = PRODUCT_NAME_IN_PRODUCT_PAGE.format(product_name)
            self.find_element(By.XPATH, xpath)
            return None
        except NoSuchElementException as e:
            return e

    def _type_in_search_input(self, text):
        try:
            input_elem = self.find_element(By.XPATH, PRODUCT_NAME_IN_CATALOG)
            input_elem.clear()
            input_elem.send_keys(text)
        except Exception as e:
            raise Exception(f"Failed to type in search input: {e}")

    def _submit_search_with_enter(self):
        try:
            input_elem = self.find_element(By.XPATH, PRODUCT_NAME_IN_CATALOG)
            input_elem.send_keys(Keys.ENTER)
        except Exception as e:
            raise Exception(f"Failed to submit search with Enter: {e}")
