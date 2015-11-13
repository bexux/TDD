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
        # setUp is not my code - path_name


class TestCheckoutProcess(FrontendTestCase):

    def get_checkoutv3(self):
        # user goes to the checkout page
        self.get_path('path_name', "/checkout/onepage/")

        # user sees the checkout form
        wait = WebDriverWait(self.driver, 60)
        element = wait.until(
            EC.visibility_of_element_located((By.ID, "onestep_form")))

    def add_product_to_cart(self, product):
        self.get_path('path_name', product)
        title = self.driver.find_element_by_css_selector('h2').text
        price = self.driver.find_element_by_css_selector(
            'span.regular-price span.price').text
        addtocart = self.driver.find_element_by_id('button-cart')
        addtocart.click()

        # user sees success message that product was added
        wait = WebDriverWait(self.driver, 60)
        element = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "ajaxcartpro-add-confirm")))
        print('Added '+title+': '+price+' to cart')

    # Form Elements
    def fill_out_billing(self):
        # Until we upgrade to PhantomJS 2, phantom is not clearing the session
        # Must clear out each input field, or the form will not submit
        # correctly

        # user enters first name
        self.driver.find_element_by_id('billing:firstname').clear()
        first_name = self.driver.find_element_by_id('billing:firstname')
        first_name.send_keys("Barbara")

        # user enters last name
        self.driver.find_element_by_id('billing:lastname').clear()
        last_name = self.driver.find_element_by_id('billing:lastname')
        last_name.send_keys("Tester")

        # user enters email address
        self.driver.find_element_by_id('billing:email').clear()
        email = self.driver.find_element_by_id('billing:email')

        # for now this is a command line prompt
        test_email = raw_input("Enter an email: ")
        email.send_keys(test_email)

        # user enters adress
        self.driver.find_element_by_id('billing:street1').clear()
        address = self.driver.find_element_by_id('billing:street1')
        address.send_keys("12345 Main St")

        # user enters city
        self.driver.find_element_by_id('billing:city').clear()
        city = self.driver.find_element_by_id('billing:city')
        city.send_keys("Beverly Hills")

        # user selects state from drop down
        state = Select(self.driver.find_element_by_id('billing:region_id'))
        state.select_by_visible_text("California")

        # user enters zipcode
        self.driver.find_element_by_id('billing:postcode').clear()
        zipcode = self.driver.find_element_by_id('billing:postcode')
        zipcode.send_keys("33067")

        # user sees country is already selected
        # mySelect = Select(self.driver.find_element_by_id('billing:country_id'))
        # option = mySelect.first_selected_option

        # user enters phone number
        self.driver.find_element_by_id('billing:telephone').clear()
        phone = self.driver.find_element_by_id('billing:telephone')
        phone.send_keys("555-555-5555")

        print('Billing information added')

    def use_billing_for_shipping_addy(self):
        # user sees "Use this address for shipping" is selected already
        shiptosame = self.driver.find_element_by_id(
            'ship_to_same_address').is_selected()
        if(shiptosame == 0):
            print('Need to click same address for shipping')

    # Shipping Options
    def detect_expedited_enabled(self, vendor):
        # wait until the progress circle stops
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(EC.invisibility_of_element_located(
            (By.ID, "loader_checkout-shipping-method-load")))

        try:
            expedited = self.driver.find_element_by_id(
                's_method_keyingredientcustom_mycarrier_expedited1')
            self.assertTrue(expedited.is_displayed)
            print 'Expedited1 is showing for '+vendor
        except:
            print 'Expedited1 does not show for '+vendor

        try:
            expedited = self.driver.find_element_by_id(
                's_method_keyingredientcustom_mycarrier_expedited2')
            self.assertTrue(expedited.is_displayed)
            print 'Expedited2 is showing for '+vendor
        except:
            print 'Expedited2 does not show for '+vendor

        try:
            expedited = self.driver.find_element_by_id(
                's_method_keyingredientcustom_mycarrier_nextday1')
            self.assertTrue(expedited.is_displayed)
            print 'NextDay1 is showing for '+vendor
        except:
            print 'NextDay1 does not show for '+vendor

        try:
            expedited = self.driver.find_element_by_id(
                's_method_keyingredientcustom_mycarrier_nextday2')
            self.assertTrue(expedited.is_displayed)
            print 'NextDay2 is showing for '+vendor
        except:
            print 'NextDay2 does not show for '+vendor

    def select_shipping_method(self, shipping_method):
        # user sees shipping options appear and selects one
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(
            EC.element_to_be_clickable((By.ID, shipping_method)))
        element.click()

        # price of shipping returned to compare to review options
        price = self.driver.find_element_by_css_selector(
            'input#'+shipping_method+' + label > span')
        price = price.text.replace('$', '')
        print('Shipping method selected: '+price)
        self.review_order(price)

    def detect_gift_card(self):
        # User sees Gift Card option and clicks it
        gcard = self.driver.find_element_by_id('giftvoucher')
        gcard.click()

        # User sees the Gift Card form appear
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "payment_form_giftvoucher")))

    def fill_out_credit_card(self):
        # User selects credit card option
        ccard = self.driver.find_element_by_id('p_method_cryozonic_stripe')
        ccard.click()

        # User enters Name
        self.driver.find_element_by_id('cryozonic_stripe_cc_owner').clear()
        ccname = self.driver.find_element_by_id('cryozonic_stripe_cc_owner')
        ccname.send_keys('Rebecca Crane')

        # User enters CC number
        self.driver.find_element_by_id('cryozonic_stripe_cc_number').clear()
        ccnum = self.driver.find_element_by_id('cryozonic_stripe_cc_number')
        ccnum.send_keys('4242424242424242')

        # User selects expiration date
        month = Select(
            self.driver.find_element_by_id('cryozonic_stripe_expiration'))
        month.select_by_visible_text('03 - March')

        year = Select(
            self.driver.find_element_by_id('cryozonic_stripe_expiration_yr'))
        year.select_by_visible_text('2022')

        # User enters cvv number
        self.driver.find_element_by_id('cryozonic_stripe_cc_cid').clear()
        cvv = self.driver.find_element_by_id('cryozonic_stripe_cc_cid')
        cvv.send_keys('123')

        # User sees Review section with shipping cost added
        print('Credit card was added. Review section updating')
        # time.sleep(30)

    def review_order(self, price):
        # user sees the new shipping method selected show up in the review
        # section
        time.sleep(30)
        shipping = self.driver.find_element_by_css_selector(
            'table#checkout-review-table tfoot tr:nth-child(2) td:nth-child(2) span'
        ).text.replace('$', '')
        assert price == shipping

    def submit_order(self):
        # User clicks submit
        submitorder = self.driver.find_element_by_id(
            'onestepcheckout_place_btn_id')
        submitorder.click()
        print('Clicked Submit')

        # Confirm order was successful
        wait = WebDriverWait(self.driver, 60)
        orderSuccess = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "h1.page-item-title")))
        assert orderSuccess.text == "Your order has been received."

    # By default, ground shipping and CC will be used
    def test_ground_guest(self):
        self.add_product_to_cart("/cuisinart-anodized-12-in-griddle/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_upsground')
        self.fill_out_credit_card()
        self.submit_order()

    def test_freeshipping_guest(self):
        self.add_product_to_cart("/actifry/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_freeshipping_freeshipping')
        self.fill_out_credit_card()
        self.submit_order()

    # Guest, Under 100, expedited shipping and CC
    def test_expedited1_guest(self):
        self.add_product_to_cart("/cuisinart-anodized-12-in-griddle/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_expedited1')
        self.fill_out_credit_card()
        self.submit_order()

    # Guest, Over 100, expedited shipping and CC
    def test_expedited2_guest(self):
        self.add_product_to_cart("/optigrill/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_expedited2')
        self.fill_out_credit_card()
        self.submit_order()

    # Guest, Under 100, next day shipping and CC
    def test_nextday1_guest(self):
        self.add_product_to_cart("/cuisinart-anodized-12-in-griddle/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_nextday1')
        self.fill_out_credit_card()
        self.submit_order()

    # Guest, Over 100, next day shipping and CC
    def test_nextday2_guest(self):
        self.add_product_to_cart("/optigrill/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_nextday2')
        self.fill_out_credit_card()
        self.submit_order()

    # Testing Expedited and Next Day do not show up for multiple vendors

    def test_expedited_vendors_vendor1(self):
        self.add_product_to_cart("/wavy-rim-bowls-cherry-4-piece/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.detect_expedited_enabled('VendorName1')

    def test_expedited_vendors_vendor2(self):
        self.add_product_to_cart("/oryx-salt-coarse-gift-pack/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.detect_expedited_enabled('VendorName2')

    def test_expedited_vendors_multiple(self):
        self.add_product_to_cart("/optigrill/")
        self.add_product_to_cart("/cuisinart-anodized-12-in-griddle/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.detect_expedited_disabled('multiple vendors')

    def test_giftcard(self):
        self.add_product_to_cart("/cuisinart-anodized-12-in-griddle/")
        self.get_checkoutv3()
        self.fill_out_billing()
        self.use_billing_for_shipping_addy()
        self.select_shipping_method(
            's_method_keyingredientcustom_mycarrier_upsground')
        self.detect_gift_card()
