import os
import sys
import requests
from lxml import html

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
tree = html.fromstring(response.content)
table = tree.xpath('/html/body/section/div/div[2]/div[2]/div/table')[0]
rows = table.xpath('.//tr')

filtered_rows = []
for row in rows:
    cols = row.xpath('.//td')
    if len(cols) >= 4:
        subject = cols[3].text_content().strip()
        if subject in TARGET_SUBJECTS:
            filtered_rows.append([col.text_content().strip() for col in cols])

with open("oktobar3.md", "w", encoding="utf-8") as f:
    f.write("| Датум | Време | Шифра | Предмет | Просторија |\n")
    f.write("|-------|-------|-------|----------|-------------|\n")
    for row in filtered_rows:
        f.write("| " + " | ".join(row) + " |\n")
