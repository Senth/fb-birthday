#!/usr/bin/python3

# Mostly copied from https://www.geeksforgeeks.org/python-automating-happy-birthday-post-on-facebook-using-selenium/

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import random

import config

random.seed(time.time())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=en-us')
  
prefs = {"profile.default_content_setting_values.notifications": 2} 
chrome_options.add_experimental_option("prefs", prefs) 
browser = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options) 

def random_user_delay():
    """Delays the script by a random amount to make us pass for a human"""
    delay = random.random() * 10.0 + 3.0
    time.sleep(delay)


# open facebook.com using get() method 
browser.get('https://mbasic.facebook.com/')
random_user_delay()

element = browser.find_elements_by_xpath('//*[@id ="m_login_email"]') 
element[0].send_keys(config.email) 
random_user_delay()
  
print("Username Entered") 
  
element = browser.find_element_by_xpath('//*[@name ="pass"]') 
element.send_keys(config.password) 
random_user_delay()
  
print("Password Entered") 
  
# logging in 
log_in = browser.find_elements_by_xpath('//*[@name ="login"]') 
log_in[0].click() 
random_user_delay()
  
print("Login Successfull") 
  
browser.get('https://mbasic.facebook.com/events/birthdays/')
random_user_delay()

birthday_article_title = "Today's Birthdays"
birthday_people_css_class = 'bk bv'
name_css_class = 'bx by bs'

def get_message(full_name):
    message = config.messages[full_name]

    # Replace with a default message
    if message in config.default_messages:
        default_messages = config.default_messages[message]
        
        # Randomize message
        message = default_messages[random.randrange(len(default_messages))]

        # Replace $ with name
        first_name = full_name.split(' ', maxsplit=1)[0]
        message = message.replace('$', first_name)

    return message

try:
    birthday_article = browser.find_element_by_xpath('.//div[@title ="' + birthday_article_title + '"]')
    birthday_people = browser.find_elements_by_xpath('.//div[@class ="' + birthday_people_css_class + '"]')


    for person in birthday_people:
        # Get name
        name_element = person.find_element_by_xpath(".//div[@class = '" + name_css_class + "']")
        full_name = name_element.text

        # Get birthday wish and post
        if full_name in config.messages:
            message = get_message(full_name)

            try:
                # Get text box
                textarea = person.find_element_by_tag_name('textarea')
                textarea.send_keys(message)
                random_user_delay()

                # Post
                post_button = person.find_element_by_xpath('.//input[@value="Post"]')
                post_button.submit()
                print(message)
                random_user_delay()

            except (ElementNotInteractableException, ElementNotVisibleException):
                print('Already posted a wish for ' + full_name)
except NoSuchElementException:
    print('No birthdays today :)')

# Close the browser 
browser.quit()
