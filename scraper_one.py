import requests
import re
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_best-selling_video_games"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")[1:]  # skip header row

def clean(text):
    text = re.sub(r"\[.*?\]", "", text)  # remove footnotes
    return text.replace("\xa0", " ").strip()

def extract_year(cells):
    """Return the first 4-digit year found in the row"""
    for cell in cells:
        match = re.search(r"\b(18|19|20)\d{2}\b", cell.get_text())
        if match:
            return match.group()
    return "Unknown"

print("\nTop 10 Best-Selling Video Games of All Time\n")
print("=" * 55)

count = 0
for row in rows:
    cells = row.find_all(["th", "td"])

    # Minimum structure: Rank | Title | Sales | ...
    if len(cells) >= 3:
        title = clean(cells[1].get_text())
        sales = clean(cells[2].get_text()) + " million"
        year = extract_year(cells)

        count += 1
        print(f"{count}. {title}")
        print(f"   Copies Sold : {sales}")
        print(f"   Release Year: {year}")
        print("-" * 55)

        if count == 10:
            break