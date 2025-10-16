import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# ===== Get page URL from environment variable =====
PAGE_URL = os.getenv("PAGE_URL")  # can rename to PAGE_URL if you like
if not PAGE_URL:
    sys.exit("❌ PAGE_URL environment variable missing")

# ===== List of target subjects in 4th column =====
TARGET_SUBJECTS = [
    "Логичко пројектовање",
    "Објектно оријентисано пројектовање",
    "Објектно оријентисано програмирање",
    "Структуре података",
    "Архитектура и организација рачунара 1",
    "Архитектура и организација рачунара 2",
    "Програмски језици"
]

# ===== Chrome setup =====
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.binary_location = "/usr/bin/chromium-browser"

browser_driver = Service("/usr/bin/chromedriver")
browser = webdriver.Chrome(service=browser_driver, options=chrome_options)

try:
    # ===== Navigate to page =====
    browser.get(PAGE_URL)

    # ===== Wait for table to appear =====
    table = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/section/div/div[2]/div[2]/div/table'))
    )

    # ===== Filter rows by 4th column =====
    rows = table.find_elements(By.TAG_NAME, "tr")
    filtered_rows = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:
            if cols[3].text in TARGET_SUBJECTS:
                filtered_rows.append([col.text for col in cols])

    # ===== Save to table.md =====
with open("table.md", "w", encoding="utf-8") as f:
    # header
    f.write("| Датум | Време | Група | Предмет | Просторија |\n")
    f.write("|-------|-------|-------|---------|------------|\n")
    # rows
    for row in filtered_rows:
        f.write(" | ".join(row) + "\n")

    print(f"✅ table.md created with {len(filtered_rows)} matching rows")

finally:
    browser.quit()
