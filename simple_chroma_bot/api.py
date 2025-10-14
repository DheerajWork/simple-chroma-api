from fastapi import FastAPI
from simple_chroma_bot import scrape_site  # ← Scraping function import
from pydantic import BaseModel

# ✅ Custom API setup
app = FastAPI(
    title="AI Agents API Collection",
    description="Dheeraj",
    version="1.0",
    docs_url="/ai-agents/docs",
    redoc_url="/ai-agents/redoc"
)
    
# ✅ Input model
class UrlInput(BaseModel):
    url: str

@app.post("/scrape")
def scrape_data(input_data: UrlInput):
    data = scrape_site(input_data.url)
    return {"message": "Scraping complete", "data": data}

# ✅ ये लाइन जरूरी है Render/Docker पर API चलाने के लिए
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=10000)
