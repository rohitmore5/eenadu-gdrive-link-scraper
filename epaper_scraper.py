import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = 'https://epaperwave.com/download-today-eenadu-epaper-pdf-in-telegu/'

def fetch_links():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    blocks = soup.find_all('p')

    for block in blocks:
        try:
            links = block.find_all('a', href=True)

            if len(links) < 2:
                continue

            ap_link = None
            ts_link = None
            date_text_raw = None

            for link in links:
                text = link.text.strip().lower()
                href = link['href']

                # Extract AP & TS links
                if "ap edition" in text:
                    ap_link = href
                    date_text_raw = text
                elif "ts edition" in text:
                    ts_link = href

            # Extract date from text like: "download 26 mar 26 ap edition"
            if date_text_raw:
                parts = date_text_raw.split()

                # Expected: ['download', '26', 'mar', '26', 'ap', 'edition']
                day = parts[1]
                month = parts[2]
                year = parts[3]

                # Convert month text → number
                month_map = {
                    "jan": "01", "feb": "02", "mar": "03",
                    "apr": "04", "may": "05", "jun": "06",
                    "jul": "07", "aug": "08", "sep": "09",
                    "oct": "10", "nov": "11", "dec": "12"
                }

                month_num = month_map.get(month.lower(), "01")

                # Convert year (26 → 2026)
                full_year = "20" + year

                formatted_date = f"{day.zfill(2)}-{month_num}-{full_year}"

                if ap_link and ts_link:
                    data.append({
                        "date": formatted_date,
                        "ap_link": ap_link,
                        "ts_link": ts_link
                    })

        except Exception:
            continue

    return data

if __name__ == "__main__":
    epapers = fetch_links()
    with open('epaper_links.json', 'w', encoding='utf-8') as f:
        json.dump(epapers, f, indent=2, ensure_ascii=False)
