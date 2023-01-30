import playwright
from playwright.sync_api import sync_playwright
from time import sleep
import requests
import json
import os

# Get the question and correct answer from OpenTDB API
amount = 1
type = 'multiple'
url = f'https://opentdb.com/api.php?amount={amount}&type={type}'
response = requests.get(url).json()
question = response['results'][0]['question']
correct_answer = response['results'][0]['correct_answer']

# Translate variables to Persian language using Playwright 
with sync_playwright() as p:  # Sync version of Playwright 

    browser = p.chromium.launch()  # Launch Chromium browser 

    page = browser.new_page()  # Create new page in the browser 

    page.goto('https://targoman.ir/')

    # Fill in the text field with the question 
    text_field = page.querySelector('.src > .false.content')
    text_field.click()
    text_field.fill(question)

    # Click on translate button 
    translate_button = page.querySelector('[src="./img/icon/copy.png"]')
    translate_button.click()
	
	translated_question = await page.evaluate(() => { return navigator.clipboard.readText(); })
	
    # Fill in the text field with the correct_answer 
    text_field2 = page.querySelector('.src > .false.content')
    text_field2.click()
    text_field2.fill(correct_answer)

    # Click on translate button 
    translate_button2 = page.querySelector('[src="./img/icon/copy.png"]')
    translate_button2.click()
	
	translated_correct_answer = await page.evaluate(() => { return navigator.clipboard.readText(); })
	
# Create a Playwright browser instance and open Twitter page 

TWITTER_USERNAME = os.environ['TWITTER_USERNAME']
TWITTER_PASSWORD = os.environ['TWITTER_PASSWORD']

browser = playwright.launch()  # Create a browser instance 
context = browser.newContext() # Create a new context for the browser instance 
page = context.newPage()       # Create a new page in the context 
page.goto('https://twitter.com/login') # Go to Twitter login page 

# Login to Twitter using Playwright 
username_input = page.querySelector('input[name="session[username_or_email]"]')   # Select username input field  
password_input = page.querySelector('input[name="session[password]"]')           # Select password input field  
username_input.fill(TWITTER_USERNAME)                                     # Fill in your username  
password_input.fill(TWITTER_PASSWORD)                                     # Fill in your password  

# Click on the Log In button to log in to Twitter account 
login_button = page.querySelector('div[data-testid="LoginForm_Login_Button"] > div > span > span')    # Select Log In button  
login_button.click()                                                             # Click on Log In button  

# Post the question and correct answer to Twitter account every 30 minutes 
while True:    

    tweetbox = page.querySelector('div[aria-label="Tweet text"]')                  # Select tweet box   

    tweetbox.fill(f"سوال: {translated_question}\nپاسخ: {translated_correct_answer}")                         # Fill in the question and correct answer into tweet box   

    postbtn = page.querySelector('div[data-testid="tweetButtonInline"] > div > span > span')     # Select post button  

    postbtn.click()                                                              # Click on post button to post the tweet  
