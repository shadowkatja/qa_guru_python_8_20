import pytest
from selene.support.shared import browser


@pytest.fixture(scope='function', autouse=True)
def set_browser():
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    browser.config.window_width = 1280
    browser.config.window_height = 1024

    yield

    browser.quit()