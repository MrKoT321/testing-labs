import time
from selenium.common.exceptions import NoSuchElementException
from config import BASE_URL


class Common:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = BASE_URL

    def open_page(self, url):
        try:
            self.driver.get(self.base_url + url)
        except Exception as e:
            raise Exception(f"Failed to open page: {e}")

    def wait_for_element(self, by, value, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                element = self.driver.find_element(by, value)
                return element
            except NoSuchElementException:
                time.sleep(0.5)
        raise Exception(f"Element not found after {timeout} seconds: ({by}, {value})")

    def wait_for_elements(self, by, value, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                elements = self.driver.find_elements(by, value)
                if elements:
                    return elements
            except NoSuchElementException:
                pass
            time.sleep(0.5)
        raise Exception(f"Elements not found after {timeout} seconds: ({by}, {value})")

    def find_element(self, by, value):
        return self.wait_for_element(by, value, timeout=10)

    def find_elements(self, by, value):
        return self.wait_for_elements(by, value, timeout=10)
