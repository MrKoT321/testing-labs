import pytest
from pages.config import LOGIN_URL, get_valid_login_data, get_invalid_login_data
from pages.auth import Auth
from abstract_test import driver, create_driver


@pytest.mark.parametrize("driver", ["chrome", "firefox"], indirect=True)
def test_successful_auth(driver):
    config = get_valid_login_data()

    auth_page = Auth(driver)
    auth_page.driver.open_page(LOGIN_URL)

    auth_page.login(config.login, config.password)
    success = auth_page.is_login_successful()

    assert success, "Ожидалась успешная авторизация, но она не прошла"
    driver.quit()


@pytest.mark.parametrize("driver", ["chrome", "firefox"], indirect=True)
def test_failed_auth(driver):
    config = get_invalid_login_data()

    auth_page = Auth(driver)
    auth_page.driver.open_page(LOGIN_URL)

    auth_page.login(config.login, config.password)
    error = auth_page.is_login_error()

    assert error, "Ожидалась ошибка авторизации, но она не появилась"
    driver.quit()
