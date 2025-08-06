import os
import json
from datetime import datetime
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")

def parse_gemini_analysis(gemini_response: str) -> dict:
    """
    Gemini'den gelen analiz metnini ayrıştırıp kullanıcı dostu formata çevirir
    """
    analysis_dict = {
        "güvenilirlik": "",
        "genel_kullanıcı_memnuniyeti": "",
        "sevilen_yönler": "",
        "sevilmeyen_yönler": "",
        "memnun_olunan_konular": "",
        "kronik_problemler": "",
        "puanlama": "",
        "alışveriş_tavsiyesi": "",
        "genel_yorumu": ""
    }
    
    # Gemini yanıtını satır satır işle
    lines = gemini_response.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Her başlığı kontrol et ve değeri al - ** karakterlerini de destekle
        if line.startswith("**Güvenilirlik:**") or line.startswith("Güvenilirlik:"):
            analysis_dict["güvenilirlik"] = line.replace("**Güvenilirlik:**", "").replace("Güvenilirlik:", "").strip()
        elif line.startswith("**Genel Kullanıcı Memnuniyeti:**") or line.startswith("Genel Kullanıcı Memnuniyeti:"):
            analysis_dict["genel_kullanıcı_memnuniyeti"] = line.replace("**Genel Kullanıcı Memnuniyeti:**", "").replace("Genel Kullanıcı Memnuniyeti:", "").strip()
        elif line.startswith("**Mağazanın sevilen yönleri:**") or line.startswith("Mağazanın sevilen yönleri:"):
            analysis_dict["sevilen_yönler"] = line.replace("**Mağazanın sevilen yönleri:**", "").replace("Mağazanın sevilen yönleri:", "").strip()
        elif line.startswith("**Mağazanın sevilmeyen yönleri:**") or line.startswith("Mağazanın sevilmeyen yönleri:"):
            analysis_dict["sevilmeyen_yönler"] = line.replace("**Mağazanın sevilmeyen yönleri:**", "").replace("Mağazanın sevilmeyen yönleri:", "").strip()
        elif line.startswith("**En çok memnun olunan konular:**") or line.startswith("En çok memnun olunan konular:"):
            analysis_dict["memnun_olunan_konular"] = line.replace("**En çok memnun olunan konular:**", "").replace("En çok memnun olunan konular:", "").strip()
        elif line.startswith("**Kronik problemleri:**") or line.startswith("Kronik problemleri:"):
            analysis_dict["kronik_problemler"] = line.replace("**Kronik problemleri:**", "").replace("Kronik problemleri:", "").strip()
        elif line.startswith("**Puanlama:**") or line.startswith("Puanlama:"):
            analysis_dict["puanlama"] = line.replace("**Puanlama:**", "").replace("Puanlama:", "").strip()
        elif line.startswith("**Alışveriş yapılmasını tavsiye eder misin:**") or line.startswith("Alışveriş yapılmasını tavsiye eder misin:"):
            analysis_dict["alışveriş_tavsiyesi"] = line.replace("**Alışveriş yapılmasını tavsiye eder misin:**", "").replace("Alışveriş yapılmasını tavsiye eder misin:", "").strip()
        elif line.startswith("**Genel gemini yorumu:**") or line.startswith("Genel gemini yorumu:"):
            analysis_dict["genel_yorumu"] = line.replace("**Genel gemini yorumu:**", "").replace("Genel gemini yorumu:", "").strip()
    
    return analysis_dict

def format_analysis_for_ui(analysis_dict: dict) -> dict:
    """
    Ayrıştırılmış analizi UI için daha güzel formatlayıp emojiler ekler
    """
    formatted = {
        "sections": [
            {
                "title": "🛡️ Güvenilirlik",
                "content": analysis_dict.get("güvenilirlik", "Veri bulunamadı"),
                "icon": "🛡️",
                "type": "security"
            },
            {
                "title": "😊 Genel Kullanıcı Memnuniyeti", 
                "content": analysis_dict.get("genel_kullanıcı_memnuniyeti", "Veri bulunamadı"),
                "icon": "😊",
                "type": "satisfaction"
            },
            {
                "title": "👍 Sevilen Yönler",
                "content": analysis_dict.get("sevilen_yönler", "Veri bulunamadı"),
                "icon": "👍",
                "type": "positive"
            },
            {
                "title": "👎 Sevilmeyen Yönler",
                "content": analysis_dict.get("sevilmeyen_yönler", "Veri bulunamadı"),
                "icon": "👎", 
                "type": "negative"
            },
            {
                "title": "🎉 En Çok Memnun Olunan Konular",
                "content": analysis_dict.get("memnun_olunan_konular", "Veri bulunamadı"),
                "icon": "🎉",
                "type": "highlight"
            },
            {
                "title": "⚠️ Kronik Problemler",
                "content": analysis_dict.get("kronik_problemler", "Veri bulunamadı"),
                "icon": "⚠️",
                "type": "warning"
            },
            {
                "title": "⭐ Puanlama",
                "content": analysis_dict.get("puanlama", "Belirsiz"),
                "icon": "⭐",
                "type": "rating"
            },
            {
                "title": "🛒 Alışveriş Tavsiyesi",
                "content": analysis_dict.get("alışveriş_tavsiyesi", "Veri bulunamadı"),
                "icon": "🛒",
                "type": "recommendation"
            },
            {
                "title": "🤖 Genel AI Yorumu",
                "content": analysis_dict.get("genel_yorumu", "Veri bulunamadı"),
                "icon": "🤖",
                "type": "summary"
            }
        ],
        "summary": {
            "rating": analysis_dict.get("puanlama", "Belirsiz"),
            "recommendation": analysis_dict.get("alışveriş_tavsiyesi", "Veri bulunamadı"),
            "total_sections": 9
        }
    }
    
    return formatted

def find_insta(site: str) -> None:
    prompt = f"""
    Bana {site} 'e ait instagram sayfasını ve hakkındaki bilgileri bul ve kullanıcı yorumlarını direkt yaz
    twitter, şikayetvar, etbis ve ekşi sözlük gibi kaynaklardan veri çek. bütün verileri istiyorum!!
    """
    try:
        response = model.generate_content(prompt)
        yorum = {
            "kaynak": "instagram",
            "site": site,
            "yorum": response.text,
            "tarih": datetime.now().isoformat()
        }
        dosya_yolu = "yorumlar_tarihli_filtreli.json"
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                mevcut_veri = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            mevcut_veri = []
        mevcut_veri.append(yorum)
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(mevcut_veri, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HATA] Gemini isteği başarısız: {str(e)}")



def ask_gemini_with_reviews(site: str, yorumlar: list[str]) -> str:
    prompt = f"""
Sen kullanıcı yorumlarına göre mağaza ve e-ticaret sitelerini değerlendiren bir müşteri asistanısın. Aşağıda "veri" adlı değişkende toplanmış farklı kaynaklardan elde edilmiş yorum ve kayıtlar var. Bu verileri dikkate alarak, her başlıktaki soruya en fazla 20 kelimeyle, kısa ve öz bir şekilde cevap ver.

Veri: {site} sitesi hakkında toplanan yorumlar ve veriler:
{chr(10).join(['- (' + yorum.get('kaynak', 'belirsiz') + ') ' + yorum['yorum'] for yorum in yorumlar if "yorum" in yorum])}

Analiz Kuralları:
• Şikayetvar: ÖZEL DEĞERLENDİRME - Şikayetvar verisi doğası gereği olumsuz olacaktır. Burada ÖNEMLİ olan:
  - Şikayet SAYISI (az şikayet = büyük firma için normal/iyi)
  - Şikayet TARİHLERİ (eski şikayetler vs güncel şikayetler)
  - Şikayet SIKLIĞI (aralıklı vs yoğun)
  - Şikayet ÇEŞİTLİLİĞİ (tek tip sorun vs çoklu sorun)
  - BÜYÜK FİRMALAR için az sayıda şikayet bile POZİTİF işaret
  - KÜÇÜK BUTİKLER için çok şikayet OLUMSUZ işaret

• Instagram/Twitter/EkşiSözlük: Bu GERÇEK KULLANICI deneyimleridir, Şikayetvar'dan çok daha değerlidir
  - Buradaki olumlu yorumlar gerçek memnuniyeti gösterir
  - Buradaki olumsuz yorumlar da gerçek sorunları gösterir
  - Bu veriler değerlendirmede ÖNCELİK almalı

• ETBİS_kayıtlı: Yasal güvenilirlik göstergesi

• Genel Kural: Instagram/Twitter/Ekşi verisi varsa bunlara AĞIRLIK ver, Şikayetvar'ı sadece YARDIMCI olarak kullan

Çıktı – Kesinlikle bu başlıkları ve sırayı koru; her cevabı 20 kelimeyi geçmeyecek şekilde yaz:

Güvenilirlik: [Cevap]
Genel Kullanıcı Memnuniyeti: [Cevap]
Mağazanın sevilen yönleri: [Cevap]
Mağazanın sevilmeyen yönleri: [Cevap]
En çok memnun olunan konular: [Cevap]
Kronik problemleri: [Cevap]
Puanlama: [Cevap]/10
Alışveriş yapılmasını tavsiye eder misin: [Cevap]
Genel gemini yorumu: [Cevap]
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[HATA] Gemini isteği başarısız: {str(e)}"

def get_formatted_analysis(site: str, yorumlar: list[str]) -> dict:
    """
    Site analizi yapar ve hem ham metni hem de formatlanmış veriyi döndürür
    """
    try:
        # Gemini'den analiz al
        raw_analysis = ask_gemini_with_reviews(site, yorumlar)
        
        # Ham metni ayrıştır
        parsed_analysis = parse_gemini_analysis(raw_analysis)
        
        # UI için formatla
        formatted_analysis = format_analysis_for_ui(parsed_analysis)
        
        # Tüm veriyi birleştir
        result = {
            "success": True,
            "site": site,
            "raw_analysis": raw_analysis,
            "parsed_data": parsed_analysis,
            "formatted_ui": formatted_analysis,
            "analysis_date": datetime.now().isoformat(),
            "comment_count": len(yorumlar)
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "site": site,
            "error": str(e),
            "analysis_date": datetime.now().isoformat()
        }


if __name__ == "__main__":
    print(find_insta("bade butik"))