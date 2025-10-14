import requests
from bs4 import BeautifulSoup
import json

url = "https://dir.indiamart.com/search.mp?ss=Toys&v=4&mcatid=20595&catid=814&crs=xnh-city"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")


data_script = soup.find("script", id="__NEXT_DATA__")
if not data_script:
    print("❌ No __NEXT_DATA__ found")
    exit()

json_data = json.loads(data_script.string)


try:
    results = json_data["props"]["pageProps"]["searchResponse"]["results"]
except KeyError:
    print(" Results key not found.")
    exit()


with open("india_mart_output.txt", "w", encoding="utf-8") as f:
    for item in results:
        fields = item.get("fields", {})
        title = fields.get("title", "N/A")
        city = fields.get("city", "N/A")

        f.write(f"Item :- {title}\nLocation :- {city}\n\n")

print(" Data saved in india_mart_output.txt")
