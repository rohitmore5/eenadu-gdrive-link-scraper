import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = 'https://epaperwave.com/download-today-eenadu-epaper-pdf-in-telegu/'

def fetch_links():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for p in soup.find_all('p', class_='has-text-align-center'):
        try:
            date_text = p.find('b').contents[0].strip().replace(":", "")
            ap_link = p.find_all('a')[0]['href']
            ts_link = p.find_all('a')[1]['href']

            data.append({
                "date": date_text,
                "ap_link": ap_link,
                "ts_link": ts_link
            })
        except Exception as e:
            continue  # Skip if structure is not as expected

    return data

if __name__ == "__main__":
    epapers = fetch_links()
    with open('epaper_links.json', 'w', encoding='utf-8') as f:
        json.dump(epapers, f, indent=2, ensure_ascii=False)
