# Base image
FROM python:3.10-slim

# Chrome aur dependencies install karna
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libgconf-2-4 \
    libx11-6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

# Chrome binary ke path set karna
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROME_DRIVER="/usr/bin/chromedriver"

# Requirements file copy karna aur install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Saare source code copy karna
COPY . .

# FastAPI app start karna (jo aapke api.py me hai)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
