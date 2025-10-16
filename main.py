import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

# ===== Environment Variables =====
LOGIN_URL = os.getenv("LOGIN_URL")
if not LOGIN_URL:
    sys.exit("❌  LOGIN_URL environment variable missing")

# ===== List of subjects to filter =====
TARGET_SUBJECTS = [
    "Логичко пројектовање",
    "Објектно оријентисано пројектовање",
    "Објектно оријентисано програмирање",
    "Структуре података",
    "Архитектура и организација рачунара 1",
    "Архитектура и организација рачунара 2",
    "Програмски језици"
]

# ===== Chrome Setup =====
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"

browser_driver = Service('/usr/bin/chromedriver')
browser = webdriver.Chrome(service=browser_driver, options=chrome_options)

try:
    # ===== Step 1: Navigate to login page =====
    browser.get(LOGIN_URL)
    time.sleep(2)

    # ===== Step 2: Locate the table =====
    table = browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div[2]/div/table')
    rows = table.find_elements(By.TAG_NAME, "tr")  # all table rows

    # ===== Step 3: Filter rows where 4th column matches target subjects =====
    filtered_rows = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:  # ensure 4th column exists
            if cols[3].text in TARGET_SUBJECTS:
                filtered_rows.append([col.text for col in cols])  # save all columns

    # ===== Step 4: Save filtered rows to Markdown =====
    with open("table.md", "w", encoding="utf-8") as f:
        for row in filtered_rows:
            f.write(" | ".join(row) + "\n")

    print(f"✅ table.md created with {len(filtered_rows)} matching rows")

finally:
    browser.quit()
