from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

LOGIN_FIELD = "login"
PASSWORD_FIELD = "password"
SUBMIT_BUTTON = ".btn-default"
SUCCESS_MESSAGE = ".alert-success"
ERROR_MESSAGE = ".alert-danger"


class Auth:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def login(self, login, password):
        try:
            login_elem = self.find_element(By.NAME, LOGIN_FIELD)
            login_elem.send_keys(login)

            pass_elem = self.find_element(By.NAME, PASSWORD_FIELD)
            pass_elem.send_keys(password)

            submit_elem = self.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON)
            submit_elem.click()
        except Exception as e:
            return e

    def is_login_successful(self):
        try:
            elem = self.find_element(By.CSS_SELECTOR, SUCCESS_MESSAGE)
            return elem.is_displayed(), None
        except NoSuchElementException as e:
            return False, e

    def is_login_error(self):
        try:
            elem = self.find_element(By.CSS_SELECTOR, ERROR_MESSAGE)
            return elem.is_displayed(), None
        except NoSuchElementException as e:
            return False, e
