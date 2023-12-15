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


def test_login():
    with step('Login with API'):
        response = demowebshop_POST_request('/login',
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

    with step('Get cookie from API'):
        cookie = response.cookies.get('NOPCOMMERCE.AUTH')

    with step('Set cookie from API'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with step('Verify successful authorization'):
        browser.element('.account').should(have.text(LOGIN))

def test_add_one_item_to_cart():
    with step('Add item through API'):
        response = demowebshop_POST_request('/addproducttocart/catalog/45/1/1')

    with step('Get cookie from API'):
        cookie = response.cookies.get('Nop.customer')

    with step('Set cookie from API'):
        browser.open('/')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open('/cart')

    with step('Check added item in cart'):
        browser.all('.cart-item-row').should(have.size(1))
        browser.element('.product-name').should(have.exact_text('Fiction'))
        browser.element('[name^="itemquantity"]').should(have.value('1'))


def test_add_two_different_items_to_cart():
    with step('Add two different items through API'):
        response = demowebshop_POST_request('/addproducttocart/catalog/45/1/1')
        cookie = response.cookies.get('Nop.customer')
        response = demowebshop_POST_request('addproducttocart/catalog/14/1/1', cookies={"Nop.customer": cookie})

    with step('Get cookie from API'):
        cookie = response.cookies.get('Nop.customer')

    with step('Set cookie from API'):
        browser.open('/')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open('/cart')

    with step('Check added item in cart'):
        browser.all('.cart-item-row').should(have.size(2))

def test_add_three_same_item_to_cart():
    with step('Add item through API'):
        response = demowebshop_POST_request('addproducttocart/details/43/1', data = {"addtocart_43.EnteredQuantity": 3})

    with step('Get cookie from API'):
        cookie = response.cookies.get('Nop.customer')

    with step('Set cookie from API'):
        browser.open('/')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open('/cart')

    with step('Check added item in cart'):
        browser.all('.cart-item-row').should(have.size(1))
        browser.element('.product-name').should(have.exact_text('Smartphone'))
        browser.element('[name^="itemquantity"]').should(have.value('3'))



