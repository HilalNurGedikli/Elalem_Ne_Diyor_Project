#!/usr/bin/env python3
# Test formatlanmış analiz sistemi

def test_parse_function():
    """Parse fonksiyonunu test et"""
    
    # Örnek Gemini yanıtı
    sample_response = """Güvenilirlik: Güvenilir site, ETBİS kayıtlı
Genel Kullanıcı Memnuniyeti: Kullanıcılar genel olarak memnun
Mağazanın sevilen yönleri: Hızlı kargo, uygun fiyat
Mağazanın sevilmeyen yönleri: Müşteri hizmetleri yavaş
En çok memnun olunan konular: Ürün kalitesi ve paketleme
Kronik problemleri: İade süreçleri uzun
Puanlama: 7/10
Alışveriş yapılmasını tavsiye eder misin: Evet, güvenle alışveriş yapabilirsiniz
Genel gemini yorumu: Orta seviye bir e-ticaret sitesi"""

    # Parse fonksiyonu
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
    
    # Yanıtı satır satır işle
    lines = sample_response.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Her başlığı kontrol et ve değeri al
        if line.startswith("Güvenilirlik:"):
            analysis_dict["güvenilirlik"] = line.replace("Güvenilirlik:", "").strip()
        elif line.startswith("Genel Kullanıcı Memnuniyeti:"):
            analysis_dict["genel_kullanıcı_memnuniyeti"] = line.replace("Genel Kullanıcı Memnuniyeti:", "").strip()
        elif line.startswith("Mağazanın sevilen yönleri:"):
            analysis_dict["sevilen_yönler"] = line.replace("Mağazanın sevilen yönleri:", "").strip()
        elif line.startswith("Mağazanın sevilmeyen yönleri:"):
            analysis_dict["sevilmeyen_yönler"] = line.replace("Mağazanın sevilmeyen yönleri:", "").strip()
        elif line.startswith("En çok memnun olunan konular:"):
            analysis_dict["memnun_olunan_konular"] = line.replace("En çok memnun olunan konular:", "").strip()
        elif line.startswith("Kronik problemleri:"):
            analysis_dict["kronik_problemler"] = line.replace("Kronik problemleri:", "").strip()
        elif line.startswith("Puanlama:"):
            analysis_dict["puanlama"] = line.replace("Puanlama:", "").strip()
        elif line.startswith("Alışveriş yapılmasını tavsiye eder misin:"):
            analysis_dict["alışveriş_tavsiyesi"] = line.replace("Alışveriş yapılmasını tavsiye eder misin:", "").strip()
        elif line.startswith("Genel gemini yorumu:"):
            analysis_dict["genel_yorumu"] = line.replace("Genel gemini yorumu:", "").strip()
    
    print("🧪 PARSE TEST RESULTS:")
    print("=" * 50)
    for key, value in analysis_dict.items():
        print(f"📊 {key}: {value}")
    print("=" * 50)
    
    # UI formatı test et
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
                "title": "⭐ Puanlama",
                "content": analysis_dict.get("puanlama", "Belirsiz"),
                "icon": "⭐",
                "type": "rating"
            }
        ],
        "summary": {
            "rating": analysis_dict.get("puanlama", "Belirsiz"),
            "recommendation": analysis_dict.get("alışveriş_tavsiyesi", "Veri bulunamadı"),
            "total_sections": 9
        }
    }
    
    print("\n🎨 UI FORMAT TEST:")
    print("=" * 50)
    for section in formatted["sections"]:
        print(f"{section['icon']} {section['title']}: {section['content']}")
    print(f"\n📊 Summary Rating: {formatted['summary']['rating']}")
    print(f"📊 Summary Recommendation: {formatted['summary']['recommendation']}")
    print("=" * 50)
    
    return analysis_dict, formatted

if __name__ == "__main__":
    print("🚀 TESTING ANALYSIS PARSING SYSTEM")
    test_parse_function()
    print("✅ Test completed!")
