from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sys
import os
from pathlib import Path

# Services klasörünü path'e ekle
services_dir = Path(__file__).parent / 'services'
sys.path.append(str(services_dir))

# Tüm service'leri import et
from site_lookup import scrape_sikayetvar
try:
    from eksi_api import scrape_eksisozluk
except ImportError:
    def scrape_eksisozluk(site_name): return []

try:
    from trendyol_api import scrape_trendyol
except ImportError:
    def scrape_trendyol(site_name): return []

try:
    from insta_api import scrape_instagram
except ImportError:
    def scrape_instagram(site_name): return []

try:
    from gemini_utils import analyze_with_gemini
except ImportError:
    async def analyze_with_gemini(data): 
        return data  # Gemini yoksa veriyi olduğu gibi döndür

try:
    from twitterdan_jsona_cek import scrape_twitter
except ImportError:
    def scrape_twitter(site_name): return []

app = FastAPI(title="Elalem API", version="1.0.0")

# CORS middleware - Chrome extension'dan gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    url: str
    site_type: str
    data: dict = None

class AnalysisResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None

def parse_site_name(site_input: str):
    """Site girdisinden site bilgilerini çıkar"""
    try:
        from urllib.parse import urlparse
        
        # Eğer URL ise parse et, değilse direkt site ismi olarak al
        if site_input.startswith(('http://', 'https://')):
            parsed_url = urlparse(site_input)
            hostname = parsed_url.netloc.lower()
        else:
            hostname = site_input.lower()
        
        # www. ve m. prefixlerini kaldır
        if hostname.startswith('www.'):
            hostname = hostname[4:]
        elif hostname.startswith('m.'):
            hostname = hostname[2:]
        
        # Domain'den site ismini çıkar
        if '.' in hostname:
            site_name = hostname.split('.')[0]
        else:
            site_name = hostname
            
        # Site türünü belirle
        site_type = "unknown"
        display_name = site_name.capitalize()
        
        if "sikayetvar" in hostname:
            site_type = "sikayetvar"
            display_name = "Şikayetvar"
        elif "eksisozluk" in hostname or "ekşisözlük" in hostname:
            site_type = "eksisozluk" 
            display_name = "Ekşi Sözlük"
        elif "instagram" in hostname:
            site_type = "instagram"
            display_name = "Instagram"
        elif "twitter" in hostname:
            site_type = "twitter"
            display_name = "Twitter"
        elif "trendyol" in hostname:
            site_type = "trendyol"
            display_name = "Trendyol"
            
        return {
            "site_name": site_name,
            "display_name": display_name,
            "site_type": site_type,
            "hostname": hostname,
            "is_supported": site_type != "unknown"
        }
        
    except Exception as e:
        return {
            "site_name": site_input,
            "display_name": site_input.capitalize(),
            "site_type": "unknown",
            "hostname": site_input,
            "is_supported": False,
            "error": str(e)
        }

@app.get("/")
async def root():
    return {"message": "Elalem API is running!"}

@app.get("/site-info")
async def get_site_info(site: str):
    """Site girişini analiz et ve bilgileri döndür"""
    try:
        site_info = parse_site_name(site)
        
        return {
            "success": True,
            "input": site,
            "data": site_info
        }
        
    except Exception as e:
        return {
            "success": False,
            "input": site,
            "error": str(e)
        }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_site(request: AnalysisRequest):
    """Chrome extension'dan gelen analiz isteklerini işle"""
    try:
        # Site bilgilerini parse et
        site_info = parse_site_name(request.url)
        site_type = site_info["site_type"]
        site_name = site_info["site_name"]
        
        result = []
        
        if site_type == "sikayetvar":
            # URL'den şirket adını çıkar
            url_parts = request.url.replace('https://www.sikayetvar.com/', '').split('/')
            company_name = url_parts[0].replace('-', '.')
            result = scrape_sikayetvar(company_name)
            
        elif site_type == "eksisozluk":
            result = scrape_eksisozluk(site_name)
            
        elif site_type == "trendyol":
            result = scrape_trendyol(site_name)
            
        elif site_type == "instagram":
            result = scrape_instagram(site_name)
            
        elif site_type == "twitter":
            result = scrape_twitter(site_name)
            
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Site type '{site_type}' not supported yet"
            )
        
        return AnalysisResponse(
            success=True,
            data={
                "site_url": request.url,
                "site_info": site_info,
                "comments": result or [],
                "comment_count": len(result) if result else 0,
                "analysis_complete": True,
                "processed_at": str(datetime.now())
            }
        )
            
    except Exception as e:
        return AnalysisResponse(
            success=False,
            error=str(e)
        )

@app.post("/analyze-data")
async def analyze_extension_data(request: AnalysisRequest):
    """Extension'dan gelen veriyi işle ve services'lere aktar"""
    try:
        # Site bilgilerini parse et
        site_info = parse_site_name(request.url)
        
        # Extension'ın topladığı veriyi al
        comments = request.data.get('comments', []) if request.data else []
        
        # Veriyi services'e aktar
        processed_data = {
            "site_info": site_info,
            "raw_comments": comments,
            "comment_count": len(comments),
            "processed_at": str(datetime.now())
        }
        
        # Site tipine göre özel işlemler
        if site_info["site_type"] == "sikayetvar":
            # Şikayet analizi için ek veriler
            processed_data["analysis_type"] = "complaint_analysis"
            processed_data["complaints"] = [
                {
                    "id": i,
                    "text": comment.get("text", ""),
                    "sentiment": "neutral",  # AI analizi eklenebilir
                    "category": "general"
                }
                for i, comment in enumerate(comments)
            ]
            
        elif site_info["site_type"] == "eksisozluk":
            # Entry analizi için ek veriler
            processed_data["analysis_type"] = "entry_analysis"
            processed_data["entries"] = [
                {
                    "id": i,
                    "text": comment.get("text", ""),
                    "topic_relevance": "high"  # AI analizi eklenebilir
                }
                for i, comment in enumerate(comments)
            ]
            
        elif site_info["site_type"] == "trendyol":
            # Ürün yorumu analizi
            processed_data["analysis_type"] = "product_review_analysis"
            processed_data["reviews"] = [
                {
                    "id": i,
                    "text": comment.get("text", ""),
                    "rating_prediction": 3.5  # AI analizi eklenebilir
                }
                for i, comment in enumerate(comments)
            ]
        
        # Burada Gemini API entegrasyonu yapılabilir
        # processed_data = await analyze_with_gemini(processed_data)
        
        return AnalysisResponse(
            success=True,
            data=processed_data
        )
        
    except Exception as e:
        return AnalysisResponse(
            success=False,
            error=str(e)
        )

@app.get("/status")
async def get_status():
    """API durumunu kontrol et"""
    return {
        "status": "healthy",
        "chrome_driver": "available",
        "services": ["sikayetvar", "eksisozluk", "instagram", "twitter", "trendyol"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
