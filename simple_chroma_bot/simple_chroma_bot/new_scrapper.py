import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def clean_text(text):
    """Clean and normalize whitespace"""
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces/newlines
    return text.strip()

def fetch_clean_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; SimpleScraper/1.0; +https://example.com/bot)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # remove unwanted tags like scripts, styles, navs, footers
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.extract()

    # extract visible text
    text = soup.get_text(separator="\n")
    lines = [clean_text(line) for line in text.splitlines() if line.strip()]
    final_text = "\n".join(lines)
    return final_text

def save_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✅] Data saved successfully in '{filename}'")

def main():
    url = input("Enter website URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print("[⏳] Fetching and formatting data... please wait...")
    try:
        formatted_text = fetch_clean_text(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"clean_data_{timestamp}.txt"
        save_to_file(formatted_text, filename)
        print("\n[✨] Done! File saved successfully.")
    except Exception as e:
        print(f"[❌] Error: {e}")

if __name__ == "__main__":
    main()
