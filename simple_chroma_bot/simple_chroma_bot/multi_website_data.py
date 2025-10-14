from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb, pandas as pd, re, json, time, os, requests
from urllib.parse import urljoin, urlparse

WAIT, MODEL, DATA, COLL, OUT = 3, "all-MiniLM-L6-v2", "./chroma_data", "webdata", "companies_output.xlsx"

def get_driver():
    o = Options()
    [o.add_argument(a) for a in ["--headless","--no-sandbox","--disable-dev-shm-usage"]]
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)

def clean(t): return re.sub(r"\s+", " ", t or "").strip() or "N/A"

def chunk(t, size=800, ov=100):
    step, res, i = size-ov, [], 0
    while i < len(t): res.append(t[i:i+size]); i += step
    return res or [t[:size]]

def serp_urls(q):
    print(f"\n🔍 Searching: {q}")
    try:
        r = requests.get("https://serpapi.com/search", params={
            "engine": "google","q": q+" official websites","num":"20",
            "api_key": "386b09e83dd3d90ff3601f443f1dd9bffbd7665030a3af8f78afd10be8fcf088"
        }).json()
        links=[]
        for i in r.get("organic_results", []):
            l=i.get("link")
            if l and not any(x in l for x in ["google","youtube","wikipedia","linkedin.com/company"]):
                d=urlparse(l).netloc
                if not any(d in u for u in links): links.append(l)
            if len(links)>=10: break
        print(f"✅ {len(links)} companies found.")
        return links
    except Exception as e:
        print("❌ Fetch error:",e); return []

def parse_addr(soup):
    for s in soup.find_all("script",type="application/ld+json"):
        try: d=json.loads(s.string or "")
        except: continue
        for i in ([d] if isinstance(d,dict) else d):
            a=i.get("address") if isinstance(i,dict) else None
            if isinstance(a,dict):
                j=", ".join([a.get(k,"") for k in ("streetAddress","addressLocality","addressRegion","postalCode","addressCountry") if a.get(k)])
                if j: return clean(j)
    return None

def contact_info(txt):
    em=re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",txt or "")
    ph=re.findall(r"\+?\d[\d\s\-]{7,}\d",txt or "")
    return (em[0] if em else "N/A"), (next((p for p in ph if re.search(r"(\+91|\d{10,13})",p)),ph[0]) if ph else "N/A")

def find_addr(soup,txt):
    for t in soup.find_all(text=re.compile(r"(Address|Location|Head Office|Contact)",re.I)):
        b=t.parent.get_text(" ",strip=True)
        if len(b)>20 and any(x in b.lower() for x in ["india","road","street","nagar","building","pune","mumbai","delhi"]): return clean(b)
    m=re.search(r"([A-Za-z0-9\s,./#-]{10,200}?(Road|Street|Nagar|Tower|Building|Sector|Area|India)[A-Za-z0-9\s,./#-]{0,120}\d{3,6})",txt or "",re.I)
    return clean(m.group(0)) if m else "N/A"

def biz_line(t):
    t=t.lower()
    if any(x in t for x in["it","software","digital","web","seo","app"]): return "IT Company"
    if "construction" in t: return "Construction"
    if any(x in t for x in["school","college","university"]): return "Educational"
    if any(x in t for x in["hospital","clinic"]): return "Healthcare"
    if "marketing" in t: return "Marketing"
    return "Business / Service Provider"

def scrape_all(prompt):
    urls=serp_urls(prompt)
    if not urls: return print("no valid website")
    os.makedirs(DATA,exist_ok=True)
    client=chromadb.PersistentClient(path=DATA)
    col=client.get_or_create_collection(COLL)
    model=SentenceTransformer(MODEL)
    d=get_driver(); rec=[]
    for u in urls:
        try:
            print(f"\n--- {u}")
            d.get(u); time.sleep(WAIT)
            s=BeautifulSoup(d.page_source,"html.parser")
            name=clean(re.sub(r"(\||\-).*","",s.title.string if s.title else "")) or urlparse(u).netloc
            a_tag=next((a['href'] for a in s.find_all('a',href=True) if 'about' in a['href'].lower()),None)
            c_tag=next((a['href'] for a in s.find_all('a',href=True) if 'contact' in a['href'].lower()),None)
            about=""
            if a_tag:
                au=a_tag if a_tag.startswith('http') else urljoin(u,a_tag)
                try:d.get(au);time.sleep(WAIT);about=clean(BeautifulSoup(d.page_source,'html.parser').get_text(' ')[:1200])
                except:about="N/A"
            else: about=clean(' '.join([p.get_text() for p in s.find_all('p')[:6]]))
            c_soup=s; c_txt=s.get_text(' ')
            if c_tag:
                cu=c_tag if c_tag.startswith('http') else urljoin(u,c_tag)
                try:d.get(cu);time.sleep(WAIT);c_soup=BeautifulSoup(d.page_source,'html.parser');c_txt=c_soup.get_text(' ')
                except: pass
            addr=parse_addr(c_soup) or parse_addr(s) or find_addr(c_soup,c_txt)
            email,phone=contact_info(c_txt)
            soc={x:"N/A" for x in["Facebook","Instagram","LinkedIn","Twitter"]}
            for a in s.find_all('a',href=True):
                h=a['href']
                if 'facebook.com'in h:soc['Facebook']=h
                if 'instagram.com'in h:soc['Instagram']=h
                if 'linkedin.com'in h:soc['LinkedIn']=h
                if any(x in h for x in ['twitter.com','x.com']):soc['Twitter']=h
            serv=[clean(x.get_text()) for x in s.find_all(['h3','h4','li']) if 4<len(x.get_text())<90]
            main=', '.join(list(dict.fromkeys(serv[:8]))) or 'N/A'
            line=biz_line(about+main)
            ch=chunk(c_txt,1000,200)
            try:
                emb=model.encode(ch).tolist()
                col.add(ids=[f"{urlparse(u).netloc}_{i}"for i in range(len(ch))],
                        documents=ch,embeddings=emb,metadatas=[{"url":u}]*len(ch))
                print(f"✅ Saved {len(ch)} chunks")
            except Exception as e: print("⚠️ Chroma error:",e)
            rec.append({'URL':u,'Business Name':name,'Business Line':line,'About Us':about,
                        'Main Products / Services':main,'Email':email,'Phone':phone,'Address':addr,
                        **soc})
        except Exception as e: print("❌ Error:",e)
    d.quit(); pd.DataFrame(rec).to_excel(OUT,index=False)
    print(f"\n📘 Done — {len(rec)} records saved to {OUT}\n💾 DB: {os.path.abspath(DATA)}")

if __name__=="__main__":
    p=input("👉 Prompt (e.g. 'top 10 IT companies in India'): ").strip() or "top 10 IT companies in India"
    scrape_all(p)
