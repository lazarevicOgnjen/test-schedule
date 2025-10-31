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
if not table:
    sys.exit("❌ No table found on the page")

rows = table.find_all("tr")
print(f"Found {len(rows)} rows in the table")

filtered_rows = []
all_subjects_found = set()

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 4:
        subject = cols[3].text.strip()
        all_subjects_found.add(subject)
        if subject in TARGET_SUBJECTS:
            filtered_rows.append([col.get_text(strip=True) for col in cols])
            print(f"✅ Matched: {subject}")

print(f"Filtered rows: {len(filtered_rows)}")
print("All subjects found on page:")
for subject in sorted(all_subjects_found):
    print(f"  - '{subject}'")

with open("oktobar3.md", "w", encoding="utf-8") as f:
    f.write("| Датум | Време | Шифра | Предмет | Просторија |\n")
    f.write("|-------|-------|-------|----------|-------------|\n")
    for row in filtered_rows:
        f.write("| " + " | ".join(row) + " |\n")

print("✅ Script completed")
