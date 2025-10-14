import requests
from bs4 import BeautifulSoup
import json

url = "https://dir.indiamart.com/search.mp?ss=Toys&v=4&mcatid=20595&catid=814&crs=xnh-city"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# __NEXT_DATA__ script tag dhundo
data_script = soup.find("script", id="__NEXT_DATA__")

if not data_script:
    print("❌ No __NEXT_DATA__ found.")
    exit()

# JSON load karo
json_data = json.loads(data_script.string)

# Pehle structure samjho (sirf ek baar run karo aur print check karo)
with open("india_mart_raw.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print("📂 Raw JSON saved as india_mart_raw.json. Open and check structure.")

# Ab products nikalne ki koshish karo
products = []
try:
    products = json_data["props"]["pageProps"]["initialState"]["search"]["products"]
except KeyError:
    print("⚠️ 'products' key not found. Check india_mart_raw.json to find correct path.")
    exit()

# File me save
with open("india_mart_output.txt", "w", encoding="utf-8") as f:
    for p in products:
        name = p.get("name", "N/A")
        location = p.get("cityName", "N/A")
        f.write(f"Item: {name}\nLocation: {location}\n---\n")

print("✅ Data saved in india_mart_output.txt")
