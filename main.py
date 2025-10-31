import os
import sys
import requests
from lxml import html

PAGE_URL = os.getenv("PAGE_URL")
if not PAGE_URL:
    sys.exit("❌ PAGE_URL environment variable missing")

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
    if len(cols) >= 8:  # Need all 8 columns
        # Check if "Модул" column (index 3) contains "3" or "4"
        module = cols[3].text_content().strip()
        if module == "3" or module == "4":
            row_values = [col.text_content().strip() for col in cols]
            print(f"✅ MATCH Row {i}: Модул = {module}")
            filtered_rows.append(row_values)

print(f"🎯 Total filtered rows: {len(filtered_rows)}")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("| Ниво | Акред. | Сем. | Модул | Шифра | Предмет | Датум | Време |\n")
    f.write("|------|--------|------|--------|--------|----------|--------|--------|\n")
    for row in filtered_rows:
        f.write("| " + " | ".join(row) + " |\n")

print("✅ Script completed - check oktobar3.md")
