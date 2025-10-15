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

# ✅ Root route (friendly message)
@app.get("/")
def root():
    return {
        "message": "API is live. Use POST /scrape with JSON body {'url': 'yourwebsite.com'}"
    }

# ✅ Input model
class UrlInput(BaseModel):
    url: str

# ✅ Scrape POST endpoint
@app.post("/scrape")
def scrape_data(input_data: UrlInput):
    try:
        data = scrape_site(input_data.url)
        return {"message": "Scraping complete", "data": data}
    except Exception as e:
        return {"message": "Error occurred", "error": str(e)}

# ✅ Render / Docker ke liye entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=10000)
