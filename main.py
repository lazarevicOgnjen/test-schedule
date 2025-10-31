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
    # ... keep your other subjects
]

response = requests.get(PAGE_URL)
tree = html.fromstring(response.content)

print("🔄 Searching for table with XPath...")
tables = tree.xpath('/html/body/section/div/div[2]/div[2]/div/table')
print(f"📊 Found {len(tables)} tables")

if not tables:
    sys.exit("❌ No table found at XPath")

table = tables[0]
rows = table.xpath('.//tr')
print(f"📈 Found {len(rows)} rows in table")

filtered_rows = []
for i, row in enumerate(rows):
    cols = row.xpath('.//td')
    if len(cols) >= 4:
        subject = cols[3].text_content().strip()
        print(f"Row {i}: Subject = '{subject}'")
        if subject in TARGET_SUBJECTS:
            print(f"✅ MATCH: {subject}")
            filtered_rows.append([col.text_content().strip() for col in cols])

print(f"🎯 Total filtered rows: {len(filtered_rows)}")

with open("oktobar3.md", "w", encoding="utf-8") as f:
    f.write("| Датум | Време | Шифра | Предмет | Просторија |\n")
    f.write("|-------|-------|-------|----------|-------------|\n")
    for row in filtered_rows:
        f.write("| " + " | ".join(row) + " |\n")

print("✅ Script completed - check oktobar3.md")
