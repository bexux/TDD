import unittest
import os
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from base import TestCase


class FrontendTestCase(TestCase):

    def setUp(self):
        #setUp not my code - path_name


class TestCouponBanner(FrontendTestCase):

    # User arrives to the homepage

    def arrive_with_coupon_with_desc(self):
        # user clicks an email and arrives on the homepage with coupon code in
        # the URL
        self.get_path('path_name', "/?coupon_code=TESTCOUPON")

        # user sees the homepage - check for Featured Products
        element = self.driver.find_element_by_class_name('home-navi')
        assert element.is_displayed

    def arrive_with_coupon_without_desc(self):
        # user clicks an email and arrives on the homepage with coupon code in
        # the URL
        self.get_path('path_name', "/?coupon_code=TESTCOUPON02")

        # user sees the homepage - check for Featured Products
        element = self.driver.find_element_by_class_name('home-navi')
        assert element.is_displayed

    def arrive_with_no_coupon(self):
        # user clicks an email and arrives on the homepage with coupon code in
        # the URL
        self.get_path('path_name', "/")

        # user sees the homepage - check for Featured Products
        element = self.driver.find_element_by_class_name('home-navi')
        assert element.is_displayed

    def get_product_page(self, product):
        # User goes to a product page
        self.get_path('path_name', product)

        # User sees the product name at the top of the page
        element = (self.driver.find_element_by_class_name('product-name'))
        assert element.is_displayed

    def add_product_to_cart(self):

        # User clickes Add to Cart button
        addtocart = self.driver.find_element_by_id('button-cart')
        addtocart.click()

        # User goes to view cart page
        # User sees success message that product was added
        wait = WebDriverWait(self.driver, 60)
        element = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "ajaxcartpro-add-confirm")))


    def get_checkoutv3(self):
        # User goes to the checkout page
        self.get_path('path_name', "/checkout/onepage/")

        # User sees the checkout form
        wait = WebDriverWait(self.driver, 60)
        element = wait.until(
            EC.visibility_of_element_located((By.ID, "onestep_form")))

    # User will see...

    def show_coupon_banner(self):
        # user sees coupon banner at the top of the page
        element = self.driver.find_element_by_class_name('couponBar')
        assert element.is_displayed

    def hide_coupon_banner(self, page, case):
        # user does not see coupon banner because there is no description for
        # that coupon code
        try:
            banner = self.driver.find_element_by_class_name(
                'couponBar')
            self.assertTrue(banneris_displayed)
            print page + ' - Error: Coupon Banner shows ' + case
        except:
            print page + ' - Pass: Coupon Bar hidden, ' + case

    def test_coupon_banner_shows(self):
        self.arrive_with_coupon_with_desc()
        self.show_coupon_banner()
        self.get_product_page("/optigrill/")
        self.show_coupon_banner()
        self.add_product_to_cart()
        self.show_coupon_banner()
        self.get_checkoutv3()
        self.hide_coupon_banner("Checkout", "not supposed to show")

    def test_coupon_banner_hides(self):
        self.arrive_with_coupon_without_desc()
        self.hide_coupon_banner("Home Page", "no description")
        self.get_product_page("/optigrill/")
        self.hide_coupon_banner("Product Page", "no description")
        self.add_product_to_cart()
        self.hide_coupon_banner("View Cart", "no description")
        self.get_checkoutv3()
        self.hide_coupon_banner("Checkout", "no description")

    def test_no_coupon_no_banner(self):
        self.arrive_with_no_coupon()
        self.hide_coupon_banner("Home Page", "no coupon")
        self.get_product_page("/optigrill/")
        self.hide_coupon_banner("Product Page", "no coupon")
        self.add_product_to_cart()
        self.hide_coupon_banner("View Cart", "no coupon")
        self.get_checkoutv3()
        self.hide_coupon_banner("Checkout", "no coupon")
