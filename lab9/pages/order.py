import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

ADD_TO_CART_BUTTON_ID = "productAdd"
ORDER_BUTTON = "a[href='cart/view']"
LOGIN_FIELD = "login"
PASSWORD_FIELD = "password"
NAME_FIELD = "name"
EMAIL_FIELD = "email"
ADDRESS_FIELD = "address"
NOTE_FIELD = "//textarea[@name='note']"
SUBMIT_BUTTON = "//button[contains(text(), 'Оформить')]"
ERROR_MESSAGE = ".alert-danger"
ERROR_TITLE = "//h1[text()='Произошла ошибка']"


class Order:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def find_element(self, by, value, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                element = self.driver.find_element(by, value)
                return element
            except NoSuchElementException:
                time.sleep(0.5)
        raise Exception(f"Element not found: ({by}, {value})")

    def add_to_cart(self):
        button = self.find_element(By.ID, ADD_TO_CART_BUTTON_ID)
        button.click()

    def click_order_button(self):
        time.sleep(2)  # как в Go-коде
        order_button = self.find_element(By.CSS_SELECTOR, ORDER_BUTTON)
        order_button.click()

    def fill_order_form(self, note):
        self._fill_field(By.XPATH, NOTE_FIELD, note)
        self._submit()

    def fill_full_order_form(self, form_data):
        self._fill_field(By.NAME, LOGIN_FIELD, form_data.login)
        self._fill_field(By.NAME, PASSWORD_FIELD, form_data.password)
        self._fill_field(By.NAME, NAME_FIELD, form_data.name)
        self._fill_field(By.NAME, EMAIL_FIELD, form_data.email)
        self._fill_field(By.NAME, ADDRESS_FIELD, form_data.address)
        self._fill_field(By.XPATH, NOTE_FIELD, form_data.note)
        self._submit()

    def is_order_made_successful(self):
        try:
            element = self.find_element(By.XPATH, ERROR_TITLE)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def is_order_made_failed(self):
        try:
            element = self.find_element(By.CSS_SELECTOR, ERROR_MESSAGE)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def _fill_field(self, by, selector, text):
        input_elem = self.find_element(by, selector)
        input_elem.clear()
        input_elem.send_keys(text)

    def _submit(self):
        submit_button = self.find_element(By.XPATH, SUBMIT_BUTTON)
        submit_button.send_keys(Keys.ENTER)
