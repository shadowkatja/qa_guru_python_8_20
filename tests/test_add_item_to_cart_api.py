import allure
from allure_commons._allure import step
from selene import have
from selene.support.shared import browser
import requests

API_URL = 'https://demowebshop.tricentis.com/'
LOGIN = 'test_api_2@test.com'
PASSWORD = '123qwe'

def demowebshop_POST_request(url, **kwargs):
    response = requests.post(API_URL + url, **kwargs)
    return response


def open_cart(self):
    browser.open('/cart')


def test_login(set_browser):
    with step("Login with API"):
        response = demowebshop_POST_request('/login',
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

    with step("Get cookie from API"):
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with step("Set cookie from API"):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))

