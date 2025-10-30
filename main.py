import os
import sys
import requests
from bs4 import BeautifulSoup

PAGE_URL = os.getenv("PAGE_URL")
if not PAGE_URL:
    sys.exit("❌ PAGE_URL environment variable missing")

TARGET_SUBJECTS = [
    "Логичко пројектовање",
    "Објектно оријентисано пројектовање",
    "Објектно оријентисано програмирање",
    "Структуре података",
    "Архитектура и организација рачунара 1",
    "Архитектура и организација рачунара 2",
    "Програмски језици",
    "Дискретна математика",
    "Вероватноћа и статистика",
    "Матрична израчунавања",
    "Базе података",
    "Теорија графова",
    "Геометријски методи и примене ",
    "Нумерички алгоритми"
]

response = requests.get(PAGE_URL)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")

filtered_rows = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 4 and cols[3].text.strip() in TARGET_SUBJECTS:
        filtered_rows.append([col.get_text(strip=True) for col in cols])

with open("oktobar3.md", "w", encoding="utf-8") as f:
    f.write("| Датум | Време | Шифра | Предмет | Просторија |\n")
    f.write("|-----|-----|-----|-----|-----|\n")
    for row in filtered_rows:
        f.write(" | ".join(row) + "\n")

