from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from routers import analyze
import uvicorn
import sys
import os
import logging
import json
from pathlib import Path

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Services klasörünü path'e ekle
services_dir = Path(__file__).parent / 'services'
sys.path.append(str(services_dir))

# Chrome Extension için gerekli import'lar
try:
    from site_lookup import scrape_sikayetvar
except ImportError:
    def scrape_sikayetvar(site_name): return []

app = FastAPI(
    title="Elalem Analytics API",
    description="Chrome Extension destekli site güvenilirlik analizi",
    version="1.0.0"
)

# CORS middleware - Chrome extension'dan gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extension için model'lar
class AnalysisRequest(BaseModel):
    url: str
    site_type: str
    data: dict = None

class AnalysisResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None

def parse_site_name(site_input: str):
    """Site girdisinden site bilgilerini çıkar - Artık tüm siteler destekleniyor"""
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
            
        # Bilinen siteler için özel isimler
        known_sites = {
            "sikayetvar": {"type": "sikayetvar", "display": "Şikayetvar"},
            "eksisozluk": {"type": "eksisozluk", "display": "Ekşi Sözlük"},
            "instagram": {"type": "instagram", "display": "Instagram"},
            "twitter": {"type": "twitter", "display": "Twitter"},
            "trendyol": {"type": "trendyol", "display": "Trendyol"},
            "facebook": {"type": "social", "display": "Facebook"},
            "youtube": {"type": "video", "display": "YouTube"},
            "google": {"type": "search", "display": "Google"},
            "amazon": {"type": "ecommerce", "display": "Amazon"},
            "netflix": {"type": "streaming", "display": "Netflix"},
            "spotify": {"type": "music", "display": "Spotify"},
            "linkedin": {"type": "social", "display": "LinkedIn"},
            "github": {"type": "development", "display": "GitHub"}
        }
        
        # Site bilgilerini belirle
        if site_name in known_sites:
            site_info = known_sites[site_name]
            site_type = site_info["type"]
            display_name = site_info["display"]
        else:
            # Bilinmeyen siteler için genel analiz
            site_type = "generic"
            display_name = site_name.capitalize()
            
        return {
            "site_name": site_name,
            "display_name": display_name,
            "site_type": site_type,
            "hostname": hostname,
            "is_supported": True,  # Artık tüm siteler destekleniyor
            "is_known_site": site_name in known_sites
        }
        
    except Exception as e:
        return {
            "site_name": site_input,
            "display_name": site_input.capitalize(),
            "site_type": "generic",
            "hostname": site_input,
            "is_supported": True,  # Hata durumunda bile analiz denenebilir
            "error": str(e)
        }

# Chrome Extension endpoint'leri
@app.get("/site-info")
async def get_site_info(site: str):
    """Chrome Extension: Site girişini analiz et ve bilgileri döndür"""
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

@app.post("/analyze-data")
async def analyze_extension_data(request: AnalysisRequest):
    """Chrome Extension: Extension'dan gelen veriyi işle"""
    logger.info(f"🔍 Chrome Extension İsteği Alındı:")
    logger.info(f"   📍 URL: {request.url}")
    logger.info(f"   🌐 Site Type: {request.site_type}")
    logger.info(f"   📊 Data Keys: {list(request.data.keys()) if request.data else 'None'}")
    
    try:
        # Site bilgilerini parse et
        site_info = parse_site_name(request.url)
        logger.info(f"   ✅ Site Info Parsed: {site_info}")
        
        # Extension'ın topladığı veriyi al
        comments = request.data.get('comments', []) if request.data else []
        logger.info(f"   💬 Extension Comments Count: {len(comments)}")
        
        # Main sistem ile entegre analiz
        from routers.analyze import analyze_site as main_analyze
        
        # Site ismini main sisteme uygun formata çevir
        site_name = site_info.get('site_name', '').replace('www.', '').replace('m.', '')
        logger.info(f"   🎯 Analyzing Site: '{site_name}'")
        
        try:
            # Ana analiz sistemini çağır
            main_result = main_analyze(site_name)
            logger.info(f"   ✅ Main Analysis Completed Successfully")
            
            response_data = {
                "extension_data": {
                    "site_info": site_info,
                    "extension_comments": comments,
                    "comment_count": len(comments)
                },
                "main_analysis": main_result,
                "processed_at": str(datetime.now())
            }
            
            logger.info(f"   📤 Returning Success Response")
            return AnalysisResponse(success=True, data=response_data)
        except Exception as main_error:
            # Ana sistem hatası durumunda sadece extension verisini döndür
            return AnalysisResponse(
                success=True,
                data={
                    "site_info": site_info,
                    "extension_comments": comments,
                    "comment_count": len(comments),
                    "main_analysis_error": str(main_error),
                    "processed_at": str(datetime.now())
                }
            )
        
    except Exception as e:
        return AnalysisResponse(
            success=False,
            error=str(e)
        )

@app.get("/test")
async def test_endpoint():
    """Test endpoint - Extension bağlantı testi"""
    logger.info("🧪 Test endpoint called")
    
    # UTF-8 encoding ile Türkçe karakterleri test edelim
    test_data = {
        "status": "success",
        "message": "API çalışıyor! Turkish chars: ğüşıöç",
        "timestamp": str(datetime.now()),
        "test_turkish": "Şımşır, çiçek, ığdır, öğrenci"
    }
    
    return JSONResponse(
        content=test_data, 
        media_type="application/json; charset=utf-8"
    )

@app.post("/analyze")
async def analyze_site_endpoint(request: AnalysisRequest):
    """Chrome Extension: Site analizi için ana endpoint"""
    logger.info(f"🚀 Extension Analyze Request:")
    logger.info(f"   📍 URL: {request.url}")
    logger.info(f"   🌐 Site Type: {request.site_type}")
    
    try:
        # URL'den site ismini çıkar
        site_info = parse_site_name(request.url)
        site_name = site_info.get('site_name', '').replace('www.', '').replace('m.', '')
        
        logger.info(f"   🎯 Extracted Site Name: '{site_name}'")
        
        # Extension'dan gelen veriyi al
        extension_data = request.data or {}
        comments = extension_data.get('comments', [])
        
        logger.info(f"   💬 Extension Data: {len(comments)} comments")
        
        # Ana analiz sistemini çağır
        try:
            from routers.analyze import analyze_site as main_analyze
            analysis_result = main_analyze(site_name)
            
            logger.info(f"   ✅ Analysis Completed Successfully")
            
            # Analiz sonucunu formatla
            response_data = {
                "site": site_info.get('display_name', site_name),
                "yorum_sayısı": len(comments),
                "analiz": analysis_result.get('analiz', 'Analiz tamamlandı'),
                "site_info": site_info,
                "processed_at": str(datetime.now())
            }
            
            logger.info(f"   📤 Sending Response: {response_data.get('site')} - {len(comments)} comments")
            
            return JSONResponse(
                content=response_data, 
                media_type="application/json; charset=utf-8"
            )
            
        except Exception as analysis_error:
            logger.error(f"   ❌ Analysis Error: {str(analysis_error)}")
            
            # Analiz hatası durumunda basit yanıt döndür
            fallback_data = {
                "site": site_info.get('display_name', site_name),
                "yorum_sayısı": len(comments),
                "analiz": f"Site analizi yapıldı. {len(comments)} yorum toplandı. Detaylı analiz için dashboard'u kontrol edin.",
                "error": "Backend analysis failed",
                "processed_at": str(datetime.now())
            }
            
            return JSONResponse(
                content=fallback_data, 
                media_type="application/json; charset=utf-8"
            )
            
    except Exception as e:
        logger.error(f"   ❌ Request Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Duplicate test endpoint removed - using the UTF-8 version above

@app.get("/status")
async def get_status():
    """API durumunu kontrol et"""
    status_data = {
        "status": "healthy",
        "mode": "main_system_integrated",
        "chrome_extension": "enabled",
        "services": ["şikayetvar", "ekşisözlük", "instagram", "twitter", "trendyol", "etbis", "gemini"],
        "encoding": "UTF-8 destekli"
    }
    
    return JSONResponse(
        content=status_data, 
        media_type="application/json; charset=utf-8"
    )

# Orijinal router'ı dahil et
app.include_router(analyze.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

