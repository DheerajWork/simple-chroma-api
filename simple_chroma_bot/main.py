import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

base_url = "https://www.saurabhinfosys.com/"
visited = set()
to_visit = [base_url]

with open("website_data.txt", "w", encoding="utf-8") as file:
    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            visited.add(url)

            file.write(f"\n{'='*80}\n")
            file.write(f"PAGE URL: {url}\n")
            file.write(f"{'='*80}\n\n")

            # Page Title------
            if soup.title and soup.title.string:
                file.write("1. PAGE TITLE\n")
                file.write(soup.title.string.strip() + "\n\n")

            # Headlines (h1, h2, h3).....
            file.write("2. HEADLINES\n")
            for tag in ["h1", "h2", "h3"]:
                for elem in soup.find_all(tag):
                    file.write(f"{tag.upper()}: {elem.get_text(strip=True)}\n")
            file.write("\n")

            # Paragraphs------
            file.write("3. PARAGRAPHS\n")
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    file.write(text + "\n")
            file.write("\n")

            # Links....
            file.write("4. LINKS\n")
            for a in soup.find_all("a", href=True):
                link = urljoin(base_url, a['href'])
                file.write(link + "\n")

                
                if link.startswith(base_url) and link not in visited:
                    to_visit.append(link)
            file.write("\n")

            time.sleep(1) 

        except Exception as e:
            print(f"Error scraping {url}: {e}")
