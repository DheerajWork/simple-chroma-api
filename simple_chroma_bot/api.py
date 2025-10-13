from fastapi import FastAPI
from simple_chroma_bot import scrape_site  # ← तुम्हारा scraping function import
from pydantic import BaseModel

# ✅ Custom API setup
app = FastAPI(
    title="AI Agents API Collection",            # 👈 Custom title
    description="Dheeraj",  # 👈 Description
    version="1.0",
    docs_url="/ai-agents/docs",                  # 👈 Custom docs URL
    redoc_url="/ai-agents/redoc"                 # 👈 Optional - Redoc UI का URL
)

# ✅ Input model
class UrlInput(BaseModel):
    url: str

@app.post("/scrape")
def scrape_data(input_data: UrlInput):
    data = scrape_site(input_data.url)
    return {"message": "Scraping complete", "data": data}
