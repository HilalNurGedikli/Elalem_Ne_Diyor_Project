from fastapi import APIRouter, Query
from services.site_lookup import scrape_sikayetvar
from services.gemini_utils import ask_gemini_with_reviews

router = APIRouter()
@router.get("/analyze")
def analyze_site(site: str = Query(..., description="Değerlendirilecek site adı")):
    yorumlar = scrape_sikayetvar(site)

    # Eğer yorumlar list değilse veya içinde yorum verisi yoksa hata döndür
    if not isinstance(yorumlar, list) or not yorumlar or not isinstance(yorumlar[0], dict):
        return {
            "site": site,
            "yorum_sayısı": 0,
            "yorumlar": yorumlar,
            "analiz": "Yorumlar çekilemedi veya sayfa bulunamadı. Lütfen site adını kontrol edin."
        }

    analiz = ask_gemini_with_reviews(site, yorumlar)
    return {
        "site": site,
        "yorum_sayısı": len(yorumlar),
        "yorumlar": yorumlar,
        "analiz": analiz
    }
