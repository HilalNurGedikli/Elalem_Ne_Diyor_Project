from fastapi import APIRouter, Query
import sys
import logging
from pathlib import Path
import json
import os
from datetime import datetime, timedelta

# Debug logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache sistemi
CACHE_FILE = "analyze_cache.json"
CACHE_DURATION_MINUTES = 30  # 30 dakika cache - aynı sitede kaldığı müddetçe

# Services klasörünü path'e ekle
services_dir = Path(__file__).parent.parent / 'services'
if str(services_dir) not in sys.path:
    sys.path.insert(0, str(services_dir))

print(f"🔧 SERVICES PATH ADDED: {services_dir}")

# Safe imports with error handling
try:
    from site_lookup import scrape_sikayetvar
    print("✅ IMPORT SUCCESS: scrape_sikayetvar")
except ImportError as e:
    print(f"❌ IMPORT FAILED: scrape_sikayetvar - {e}")
    def scrape_sikayetvar(site): 
        print(f"⚠️  FALLBACK: scrape_sikayetvar called for {site}")
        return []

try:
    from twitterdan_jsona_cek import twitter_yorum_ekle
    print("✅ IMPORT SUCCESS: twitter_yorum_ekle")
except ImportError as e:
    print(f"❌ IMPORT FAILED: twitter_yorum_ekle - {e}")
    def twitter_yorum_ekle(site): 
        print(f"⚠️  FALLBACK: twitter_yorum_ekle called for {site}")
        return []

try:
    from gemini_utils import ask_gemini_with_reviews
    print("✅ IMPORT SUCCESS: ask_gemini_with_reviews")
except ImportError as e:
    print(f"❌ IMPORT FAILED: ask_gemini_with_reviews - {e}")
    def ask_gemini_with_reviews(site, yorumlar): 
        print(f"⚠️  FALLBACK: ask_gemini_with_reviews called for {site}")
        return "Gemini analizi şu anda kullanılamıyor."
try:
    from gemini_utils import find_insta
    print("✅ IMPORT SUCCESS: find_insta")
except ImportError as e:
    print(f"❌ IMPORT FAILED: find_insta - {e}")
    def find_insta(site): 
        print(f"⚠️  FALLBACK: find_insta called for {site}")
        return "Gemini analizi insta şu anda kullanılamıyor."

try:
    from gemini_utils import find_insta
    print("✅ IMPORT SUCCESS: find_insta")
except ImportError as e:
    print(f"❌ IMPORT FAILED: find_insta - {e}")
    def find_insta(site): 
        print(f"⚠️  FALLBACK: find_insta called for {site}")
        return "Instagram analizi şu anda kullanılamıyor."

try:
    from eksi_api import scrape_eksi
    print("✅ IMPORT SUCCESS: scrape_eksi")
except ImportError as e:
    print(f"❌ IMPORT FAILED: scrape_eksi - {e}")
    def scrape_eksi(site, max_pages=5): 
        print(f"⚠️  FALLBACK: scrape_eksi called for {site}")
        return []

try:
    from etbis_kayitlimi import etbis_kayit_kontrol, yorumu_jsona_ekle
    print("✅ IMPORT SUCCESS: etbis functions")
except ImportError as e:
    print(f"❌ IMPORT FAILED: etbis functions - {e}")
    def etbis_kayit_kontrol(site): 
        print(f"⚠️  FALLBACK: etbis_kayit_kontrol called for {site}")
        return "Site kayıtlı değil"
    def yorumu_jsona_ekle(etbis_sonuc): 
        print(f"⚠️  FALLBACK: yorumu_jsona_ekle called")
        return None

# Root directory'den yorumlari_json_oku import et
try:
    import sys
    root_dir = Path(__file__).parent.parent
    sys.path.append(str(root_dir))
    from yorumlari_json_oku import yorumlari_oku
except ImportError:
    def yorumlari_oku(): return []

# Cache fonksiyonları
def load_cache():
    """Cache dosyasını yükle"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"❌ CACHE LOAD ERROR: {e}")
        return {}

def save_cache(cache_data):
    """Cache dosyasına kaydet"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"✅ CACHE SAVED")
    except Exception as e:
        print(f"❌ CACHE SAVE ERROR: {e}")

def is_cache_valid(timestamp_str):
    """Cache'in hala geçerli olup olmadığını kontrol et"""
    try:
        cache_time = datetime.fromisoformat(timestamp_str)
        current_time = datetime.now()
        return (current_time - cache_time) < timedelta(minutes=CACHE_DURATION_MINUTES)
    except:
        return False

def get_cached_result(site):
    """Site için cache'lenmiş sonucu getir"""
    cache = load_cache()
    site_key = site.lower().strip()
    
    if site_key in cache:
        cached_entry = cache[site_key]
        if is_cache_valid(cached_entry.get('timestamp', '')):
            print(f"🎯 CACHE HIT: Using cached result for '{site}'")
            return cached_entry['result']
        else:
            print(f"⏰ CACHE EXPIRED: Cache expired for '{site}'")
            # Eski cache'i temizle
            del cache[site_key]
            save_cache(cache)
    
    print(f"🔍 CACHE MISS: No valid cache for '{site}'")
    return None

def save_result_to_cache(site, result):
    """Sonucu cache'e kaydet"""
    cache = load_cache()
    site_key = site.lower().strip()
    
    cache[site_key] = {
        'result': result,
        'timestamp': datetime.now().isoformat()
    }
    
    save_cache(cache)
    print(f"💾 RESULT CACHED for '{site}'")

router = APIRouter()

@router.get("/analyze")
def analyze_site(site: str = Query(..., description="Değerlendirilecek site adı")):
    print(f"\n🚀 ANALYZE SITE STARTED: {site}")
    print("=" * 50)
    
    # Cache kontrolü
    cached_result = get_cached_result(site)
    if cached_result:
        print(f"📤 RETURNING CACHED RESULT for '{site}'")
        print(f"   📊 Cached Yorum Sayısı: {cached_result.get('yorum_sayısı', 0)}")
        print(f"   📊 Cached Analiz Length: {len(str(cached_result.get('analiz', '')))}")
        print("=" * 50)
        return cached_result
    
    print(f"🔄 STARTING FRESH ANALYSIS for '{site}'...")
    
    # 1. Şikayetvar Scraping
    print(f"📋 1. ŞIKAYETVAR SCRAPING for '{site}'...")
    try:
        sikayetvar_result = scrape_sikayetvar(site)
        print(f"✅ ŞIKAYETVAR COMPLETED - Result type: {type(sikayetvar_result)}")
        if isinstance(sikayetvar_result, list):
            print(f"   📊 Found {len(sikayetvar_result)} items")
        else:
            print(f"   📊 Result: {sikayetvar_result}")
    except Exception as e:
        print(f"❌ ŞIKAYETVAR ERROR: {e}")
    
    # 2. ETBİS Kontrol
    print(f"\n🏢 2. ETBİS KONTROL for '{site}'...")
    try:
        etbis_sonuc = etbis_kayit_kontrol(site)
        print(f"✅ ETBİS KONTROL COMPLETED")
        print(f"   📊 ETBİS Result: {etbis_sonuc}")
        
        # ETBİS sonucunu JSON'a ekle
        print(f"📝 3. ETBİS -> JSON...")
        yorumu_jsona_ekle_result = yorumu_jsona_ekle(etbis_sonuc)
        print(f"✅ ETBİS JSON EKLEME COMPLETED")
        print(f"   📊 JSON Result: {yorumu_jsona_ekle_result}")
        
    except Exception as e:
        print(f"❌ ETBİS ERROR: {e}")
    
    # 3. Instagram Verisi
    print(f"\n📸 3. INSTAGRAM VERİSİ for '{site}'...")
    try:
        instagram_result = find_insta(site)
        print(f"✅ INSTAGRAM COMPLETED")
        print(f"   📊 Instagram Result: {instagram_result}")
    except Exception as e:
        print(f"❌ INSTAGRAM ERROR: {e}")

    # 4. Twitter Yorumları
    print(f"\n🐦 4. TWITTER YORUMLARI for '{site}'...")
    try:
        twitter_result = twitter_yorum_ekle(site)
        print(f"✅ TWITTER COMPLETED")
        print(f"   📊 Twitter Result: {twitter_result}")
    except Exception as e:
        print(f"❌ TWITTER ERROR: {e}")

    # 5. Ekşi Sözlük
    print(f"\n📚 5. EKŞİ SÖZLÜK for '{site}'...")
    try:
        eksi_result = scrape_eksi(site, max_pages=5)
        print(f"✅ EKŞİ COMPLETED")
        if isinstance(eksi_result, list):
            print(f"   📊 Found {len(eksi_result)} entries")
        else:
            print(f"   📊 Result: {eksi_result}")
    except Exception as e:
        print(f"❌ EKŞİ ERROR: {e}")
    
    # 6. Yorumları Oku
    print(f"\n📖 6. YORUMLARI OKU...")
    try:
        yorumlar = yorumlari_oku()
        print(f"✅ YORUMLAR OKUNDU")
        print(f"   📊 Type: {type(yorumlar)}")
        if isinstance(yorumlar, list):
            print(f"   📊 Count: {len(yorumlar)}")
            if yorumlar and len(yorumlar) > 0:
                print(f"   📊 First item type: {type(yorumlar[0])}")
                if isinstance(yorumlar[0], dict):
                    print(f"   📊 First item keys: {list(yorumlar[0].keys())}")
        else:
            print(f"   📊 Content: {yorumlar}")
    except Exception as e:
        print(f"❌ YORUMLARI OKU ERROR: {e}")
        yorumlar = []

    
    # 7. Yorumları Validate Et
    print(f"\n🔍 7. YORUMLAR VALİDASYON...")
    if not isinstance(yorumlar, list) or not yorumlar or not isinstance(yorumlar[0], dict):
        print(f"❌ YORUMLAR VALİDASYON FAILED")
        print(f"   📊 Is list: {isinstance(yorumlar, list)}")
        print(f"   📊 Has content: {bool(yorumlar)}")
        if yorumlar:
            print(f"   📊 First item is dict: {isinstance(yorumlar[0], dict)}")
        
        result = {
            "site": site,
            "yorum_sayısı": 0,
            "yorumlar": yorumlar,
            "analiz": "Yorumlar çekilemedi veya sayfa bulunamadı. Lütfen site adını kontrol edin."
        }
        print(f"\n📤 RETURNING ERROR RESULT (NOT CACHED): {result}")
        print("=" * 50)
        return result
    
    print(f"✅ YORUMLAR VALİDASYON SUCCESS - {len(yorumlar)} valid comments")
    
    # 8. Gemini Analizi
    print(f"\n🤖 8. GEMİNİ ANALİZİ...")
    try:
        analiz = ask_gemini_with_reviews(site, yorumlar)
        print(f"✅ GEMİNİ ANALİZİ COMPLETED")
        print(f"   📊 Analysis length: {len(str(analiz))}")
        print(f"   📊 Analysis preview: {str(analiz)[:100]}...")
    except Exception as e:
        print(f"❌ GEMİNİ ANALİZİ ERROR: {e}")
        analiz = f"Analiz hatası: {e}"
    
    # 9. Final Result
    final_result = {
        "site": site,
        "yorum_sayısı": len(yorumlar),
        "yorumlar": yorumlar,
        "analiz": analiz
    }
    
    # Sonucu cache'e kaydet
    save_result_to_cache(site, final_result)
    
    print(f"\n🎯 FINAL RESULT:")
    print(f"   📊 Site: {final_result['site']}")
    print(f"   📊 Yorum Sayısı: {final_result['yorum_sayısı']}")
    print(f"   📊 Analiz Length: {len(str(final_result['analiz']))}")
    print("=" * 50)
    
    return final_result
