import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

# Get login page URL from environment variable
LOGIN_URL = os.getenv("LOGIN_URL")
if not LOGIN_URL:
    sys.exit("❌  LOGIN_URL environment variable missing")

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"

# Chrome driver setup
browser_driver = Service('/usr/bin/chromedriver')
browser = webdriver.Chrome(service=browser_driver, options=chrome_options)

try:
    # Step 1: Navigate to login page (from user input)
    browser.get(LOGIN_URL)
    time.sleep(2)

    # Step 2: Extract content
    response = browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div[2]/div/table')
    table_text = response.text

    # Save to markdown
    with open("table.md", "w") as f:
        f.write(table_text)

finally:
    browser.quit()
