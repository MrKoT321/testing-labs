import pytest
from selenium import webdriver
from pages.config import BASE_URL


def create_driver(browser_name):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    return webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )


@pytest.fixture
def driver(request):
    browser_name = request.param
    driver = create_driver(browser_name)
    yield driver
    driver.quit()
