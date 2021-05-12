from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession, AsyncHTMLSession
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import schedule
import time
import config

# Add function that finds the product on the website via Search or category pages and gives this url to check_availability()
# def findProduct():
#     session = init()
#     overview_page = session.get('https://www.coolblue.nl/consoles')
#     overview_page.html.find('', first=True)

# Checks if the page contains a Add to cart button
def check_availability():
    session = HTMLSession()
    productpage = session.get(config.product_link)
    buy_button = productpage.html.find('input[class="js-shopping-cart-input"]', first=True)
    return (buy_button is not None)

# Add product to cart
def add_to_cart():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/bin/chromedriver")
    driver.implicitly_wait(10)

    # Navigate to productpage
    driver.get(config.product_link)

    # Accept cookies on productpage
    cookie_button = driver.find_element_by_name("accept_cookie")
    cookie_button.click()
    print('Passed Cookie')

    # Add to cart on productpage
    cart_button = driver.find_element_by_class_name("js-add-to-cart-button")
    cart_button.click()
    print('Added to cart')

    # Cart page
    time.sleep(1)
    driver.get('https://www.coolblue.nl/winkelmandje')
    checkout_button = driver.find_elements_by_name('checkout')
    checkout_button[1].click()
    print('Passed Cart')

    # Checkout 1 - Confirm emailadress
    driver.find_element_by_id('email_address_loginmethod').send_keys(config.email)
    driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/form/div[2]/button').click()
    print('Passed Email')

    # Checkout 1 - Fill in details
    driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[4]/div/div[2]/div[1]/label').click()
    driver.find_element_by_name('shipment_address_first_name').send_keys(config.firstname)
    driver.find_element_by_name('shipment_address_last_name').send_keys(config.lastname)
    driver.find_element_by_name('shipment_address_post_code').send_keys(config.zipcode)
    driver.find_element_by_name('shipment_address_house_number').send_keys(config.housenumber)
    driver.find_element_by_name('phone_number').send_keys(config.phonenumber)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(config.password)
    driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(config.password)
    driver.find_element_by_class_name('js-postal-code-result-view--edit').click()
    driver.find_element_by_name('shipment_address_street').clear()
    driver.find_element_by_name('shipment_address_city').clear()
    driver.find_element_by_name('shipment_address_street').send_keys(config.street)
    driver.find_element_by_name('shipment_address_city').send_keys(config.city)
    driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[14]/div[2]/div/div/div[2]/button').click()
    print('Filled in details')

    # Checkout 3 - Choose shipping method
    driver.find_elements_by_name('save_order')[2].click()
    print('Passed Shipping')

    # Checkout 4 - Choose bank
    driver.find_element_by_class_name('js-toggle-form-field-content-container-payment').find_element_by_tag_name('button').click()
    driver.find_elements_by_class_name('radio-button__radio')[1].click()
    driver.find_element_by_class_name('js-ideal-issuer-submit').click()
    print('Passed Bank')

    # Finish page
    driver.find_elements_by_name('save_order')[1].click()
    print('Passed CoolBlue')

    # ASN
    driver.find_elements_by_class_name('accordion__heading')[1].click()
    print('Passed ASN')

def main():
    if check_availability():
        print('Available')
        add_to_cart()
        schedule.clear()
        print('Finished')
    else:
        print('Not available, will retry...')

schedule.every(1).seconds.do(main)

while True:
    schedule.run_pending()