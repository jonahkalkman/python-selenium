from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession, AsyncHTMLSession
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from os import system
import os
import schedule
import time
import config
import urllib


# Checks if the page contains a Add to cart button
def check_availability():
    print('started')
    session = HTMLSession()
    print('started session')
    productpage = session.get(config.product_link)
    print(productpage.status_code)
    buy_button = productpage.html.xpath("/html/body/main/div/article/div/div[3]/section[1]/button", first=True)
    return (buy_button is not None)

def retry_click(element):
    try:
        element.click()
    except:
        retry_click(element)

# Add product to cart
def add_to_cart():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/bin/chromedriver")
    driver.implicitly_wait(5)

    # Navigate to productpage
    driver.get(config.product_link)

    # Accept cookies on productpage
    cookie_button = driver.find_element_by_class_name("cookiewall__accept-btn")
    retry_click(cookie_button)
    print('Passed Cookie')

    # Add to cart on productpage
    cart_button = driver.find_element_by_class_name("productoffer__orderbtn")
    retry_click(cart_button)
    print('Added to cart')

    # Cart page
    time.sleep(2)
    driver.get('https://www.bcc.nl/bestellen/winkelwagen')
    element = driver.find_element_by_xpath('/html/body/app-root/app-shopping-cart/div/div/div[1]/div[2]/div[1]/div[2]/button')
    retry_click(element)
    print('Passed Cart')

    # Checkout 1 - Delivery
    driver.find_element_by_name('zipcode').send_keys(config.zipcode)
    continue_button = driver.find_element_by_xpath('/html/body/app-root/app-delivery/div/div/div[1]/div/div/div[2]/button')
    retry_click(continue_button)
    print('Passed delivery')

    # Checkout 1 - Fill in details
    driver.find_element_by_name('firstname').send_keys(config.firstname)
    driver.find_element_by_name('surname').send_keys(config.lastname)
    driver.find_element_by_id('address1HouseNumber').send_keys(config.housenumber)
    driver.find_element_by_name('phone').send_keys(config.phonenumber)
    driver.find_element_by_name('email').send_keys(config.email)

    checkout_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'continue-btn')))
    retry_click(checkout_button)
    print('Filled in details')

    # Checkout 3 - Choose bank
    bank_select = driver.find_element_by_name('bank')
    retry_click(bank_select)

    for option in bank_select.find_elements_by_tag_name('option'):
        if option.text == "ASN Bank":
            retry_click(option)

    finish_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue-btn')))
    retry_click(finish_button)
    print('Passed choose bank')

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