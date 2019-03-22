#!/usr/bin/python3

# Mostly copied from https://www.geeksforgeeks.org/python-automating-happy-birthday-post-on-facebook-using-selenium/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
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
browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options) 
  
# open facebook.com using get() method 
browser.get('https://mbasic.facebook.com/')

# user_name or e-mail id 
username = "senth.wallace@gmail.com"

element = browser.find_elements_by_xpath('//*[@id ="m_login_email"]') 
element[0].send_keys(username) 
  
print("Username Entered") 
  
element = browser.find_element_by_xpath('//*[@name ="pass"]') 
element.send_keys(config.password) 
  
print("Password Entered") 
  
# logging in 
log_in = browser.find_elements_by_xpath('//*[@name ="login"]') 
log_in[0].click() 
  
print("Login Successfull") 
  
browser.get('https://mbasic.facebook.com/events/birthdays/')

birthday_article_title = "Today's Birthdays"
birthday_people_css_class = 'bk bv'
name_css_class = 'bx by bs'

birthday_article = browser.find_element_by_xpath('.//div[@title ="' + birthday_article_title + '"]')
birthday_people = browser.find_elements_by_xpath('.//div[@class ="' + birthday_people_css_class + '"]')

def printRaw(text):
    text = text + '\n'
    sys.stdout.buffer.write(text.encode('utf8'))

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

            # Post
            post_button = person.find_element_by_xpath('.//input[@value="Post"]')
            post_button.submit()
            print(message)

            time.sleep(5)
        except ElementNotInteractableException:
            print('Already posted a wish for ' + full_name)

# Close the browser 
browser.quit()
