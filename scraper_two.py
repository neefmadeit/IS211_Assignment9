import requests
import re
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Jamaican_records_in_athletics"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

def clean(text):
    text = re.sub(r"\[.*?\]", "", text)  # remove footnotes
    return text.replace("\xa0", " ").strip()

sprinters = []

# Loop through all tables
for table in soup.find_all("table", class_="wikitable"):
    headers_row = table.find("tr")
    if not headers_row:
        continue

    headers = [th.get_text(strip=True) for th in headers_row.find_all("th")]

    # We ONLY want tables that clearly list athletes
    if "Athlete" not in headers or "Event" not in headers:
        continue

    athlete_idx = headers.index("Athlete")
    event_idx = headers.index("Event")

    rows = table.find_all("tr")[1:]

    for row in rows:
        cells = row.find_all("td")
        if len(cells) <= max(athlete_idx, event_idx):
            continue

        event = clean(cells[event_idx].get_text())

        # Restrict to men’s short sprints
        if event not in ("100 m", "200 m"):
            continue

        athlete = clean(cells[athlete_idx].get_text())

        if athlete and athlete not in sprinters:
            sprinters.append(athlete)

# Print Top 10
print("\nTop 10 Jamaican Men Sprinters\n")
print("=" * 40)

for i, name in enumerate(sprinters[:10], start=1):
    print(f"{i}. {name}")