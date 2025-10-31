import os
import sys
import requests
from lxml import html

PAGE_URL = os.getenv("PAGE_URL")
if not PAGE_URL:
    sys.exit("❌ PAGE_URL environment variable missing")

response = requests.get(PAGE_URL)
tree = html.fromstring(response.content)

tables = tree.xpath('/html/body/section/div/div[2]/div[2]/div/table')
if not tables:
    sys.exit("❌ No table found at XPath")

table = tables[0]
rows = table.xpath('.//tr')

filtered_rows = []
for row in rows:
    cols = row.xpath('.//td')
    if len(cols) >= 8:
        row_values = [col.text_content().strip() for col in cols]
        if ("3" in row_values or "4" in row_values) and "РИИ" in row_values:
            filtered_rows.append(row_values)

with open("oktobar3.md", "w", encoding="utf-8") as f:
    f.write("| Ниво | Акред. | Сем. | Модул | Шифра | Предмет | Датум | Време |\n")
    f.write("|------|--------|------|--------|--------|----------|--------|--------|\n")
    for row in filtered_rows:
        f.write("| " + " | ".join(row) + " |\n")
