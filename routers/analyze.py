from fastapi import APIRouter, Query
from services.site_lookup import scrape_sikayetvar
from services.gemini_utils import ask_gemini_with_reviews

router = APIRouter()

@router.get("/analyze")
def analyze_site(site: str = Query(..., description="Değerlendirilecek site adı")):
    yorumlar = scrape_sikayetvar(site)

    if not yorumlar or yorumlar[0].startswith("[HATA]"):
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
