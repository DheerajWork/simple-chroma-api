from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Chrome headless mode options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")  # Full HD for proper rendering

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = "https://dir.indiamart.com/search.mp?ss=computer&v=4&mcatid=20595&catid=814&cityid=70472&crs=city-landing&trc=xium&cq=ahmedabad&tags=res:RC3|ktp:N0|mtp:G|wc:1|lcf:3|cq:ahmedabad|qr_nm:gl-gd|cs:17025|com-cf:nl|ptrs:na|mc:26343|cat:57|qry_typ:P|lang:en|tyr:1|qrd:250920|mrd:250919|prdt:250920|msf:ms|pfen:1|gli:G1I2|gc:Sikar|ic:Jodhpur|scw:1|lf:4"
    driver.get(url)

    # Wait for page to load completely
    time.sleep(15)

    # Scroll down to trigger lazy loading
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # wait for lazy loading
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find product elements
    products = driver.find_elements(By.CSS_SELECTOR, ".prd-listing")

    if not products:
        print("❌ No products found. Please check selectors or page load.")
    else:
        product_list = []
        for product in products[:20]:
            name = product.find_elements(By.CSS_SELECTOR, "a.prd-name")
            price = product.find_elements(By.CSS_SELECTOR, "span.prd-price")
            company = product.find_elements(By.CSS_SELECTOR, "span.cmpny-name")
            location = product.find_elements(By.CSS_SELECTOR, "span.loc")

            product_list.append({
                "Name": name[0].text if name else "N/A",
                "Price": price[0].text if price else "N/A",
                "Company": company[0].text if company else "N/A",
                "Location": location[0].text if location else "N/A"
            })

        # Save to Excel
        df = pd.DataFrame(product_list)
        df.to_excel("indiamart_products_headless.xlsx", index=False)
        print(f"✅ Total products saved: {len(product_list)}")

finally:
    driver.quit()
