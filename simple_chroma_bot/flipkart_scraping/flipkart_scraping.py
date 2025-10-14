from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

url = "https://www.flipkart.com/search?q=i+phone+17"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

wait = WebDriverWait(driver, 20)

# Close login popup if it appears
try:
    close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="✕"]')))
    close_btn.click()
    print("Closed login popup ✅")
except:
    print("No login popup ✅")

time.sleep(3)

# Scroll to load all products
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Product name
product_elements = driver.find_elements(By.XPATH, '//div[@class="KzDlHZ"]')
if not product_elements:
    product_elements = driver.find_elements(By.XPATH, '//a[@class="wjcEIp"]')

# Price
price_elements = driver.find_elements(By.XPATH, '//div[contains(@class,"Nx9bqj")]')

# Discount
discount_elements = driver.find_elements(By.XPATH, '//div[contains(@class,"UkUFwK")]')

# Features
feature_elements = driver.find_elements(By.XPATH, '//ul[@class="G4BRas"]')

products = [p.text for p in product_elements]
prices = [p.text for p in price_elements]
discounts = [d.text for d in discount_elements]
features = [f.text.replace("\n", " | ") for f in feature_elements]

driver.quit()

# --- Fix: pad all lists to same length ---
max_len = max(len(products), len(prices), len(discounts), len(features))

def pad_list(lst, size):
    return lst + [""] * (size - len(lst))

products = pad_list(products, max_len)
prices = pad_list(prices, max_len)
discounts = pad_list(discounts, max_len)
features = pad_list(features, max_len)

# Save to Excel
df = pd.DataFrame({
    "Product Name": products,
    "Price": prices,
    "Discount": discounts,
    "Features": features
})

df.to_excel("flipkart_products.xlsx", index=False, engine="openpyxl")

print(f"✅ Scraped {len(products)} products with Price, Discount & Features. Saved to flipkart_products.xlsx")
