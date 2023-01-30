import playwright
from playwright import sync_playwright
from time import sleep
import requests
import json
import os

# Get question and correct answer from OpenTDB API 
url = 'https://opentdb.com/api.php?amount=1&type=multiple' 
response = requests.get(url) 
data = json.loads(response.text) 
question = data['results'][0]['question'] 
correct_answer = data['results'][0]['correct_answer'] 

# Translate variables to Persian language using Playwright 
with playwright.chromium.connect() as browser: 
    page = await browser.newPage() 

    await page.goto('https://translate.google.com/')

    await page.fill('input[name="text"]', question)

    await page.selectOption('select[name="sl"]', 'en')

    await page.selectOption('select[name="tl"]', 'fa')

    await page.click('input[type="submit"]')

    translated_question = await page.$eval('span#result_box', el => el.innerText)

    # Translate correct answer to Persian language using Playwright 
    await page.fill('input[name="text"]', correct_answer)

    await page.selectOption('select[name="sl"]', 'en')

    await page.selectOption('select[name="tl"]', 'fa')

    await page.click('input[type="submit"]')

    translated_correct_answer = await page.$eval('span#result_box', el => el.innerText)  
	
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
