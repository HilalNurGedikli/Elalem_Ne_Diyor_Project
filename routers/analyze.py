from fastapi import APIRouter, Query
from services.site_lookup import scrape_sikayetvar
from services.twitterdan_jsona_cek import twitter_yorum_ekle
from services.gemini_utils import ask_gemini_with_reviews
from yorumlari_json_oku import yorumlari_oku
from services.etbis_kayitlimi import etbis_kayit_kontrol,yorumu_jsona_ekle
router = APIRouter()
@router.get("/analyze")
def analyze_site(site: str = Query(..., description="Değerlendirilecek site adı")):
    scrape_sikayetvar(site)
    print("şikayetvar bittti")
    etbis_sonuc = etbis_kayit_kontrol(site)
    print("etbis okey")
    yorumu_jsona_ekle(etbis_sonuc)
    twitter_yorum_ekle(site)
    print ("tw okwy")
    yorumlar= yorumlari_oku()

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
