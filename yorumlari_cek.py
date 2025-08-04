from bs4 import BeautifulSoup
import re
import json
import uuid
from datetime import datetime

# Türkçe aylar sözlüğü
aylar = {
    "ocak": "01", "şubat": "02", "mart": "03", "nisan": "04", "mayıs": "05", "haziran": "06",
    "temmuz": "07", "ağustos": "08", "eylül": "09", "ekim": "10", "kasım": "11", "aralık": "12"
}

# Anahtar kelimeler
anahtar_kelimeler = [
    "şikayet", "şikayetçi", "memnun değilim", "pişman", "iade", "ret", "reddedildi",
    "yırtıldı", "kırıldı", "soyuldu", "çatladı", "şikayetim", "kalitesiz", "hüsran",
    "yanıltıcı", "bozuldu", "incelendi", "olumsuz", "reddi", "değişim yapılmadı",
    "memnun", "teşekkür", "çok beğendim", "sorunsuz", "iyi hizmet", "kaliteli",
    "hızlı teslimat", "olumlu", "tavsiye ederim", "güzel", "iyi ki", "harika", "çok güzel",
    "beğendim", "mükemmel", "tatmin oldum", "şahane", "kusursuz"
]

# HTML yükle
with open("sayfa.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

filtreli_yorumlar = []
articles = soup.find_all("article")

for article in articles:
    try:
        p_tag = article.find("p")
        if not p_tag:
            continue

        yorum = p_tag.get_text(strip=True).lower()
        if not any(kelime in yorum for kelime in anahtar_kelimeler):
            continue

        tarih_iso = None

        # 1️⃣ Div içinden tarihi çekmeye çalış
        tarih_div = article.find("div", class_="js-tooltip time")
        if tarih_div:
            tarih_text = tarih_div.get_text(strip=True).lower()
            try:
                parcalar = tarih_text.split()
                if len(parcalar) >= 3:
                    gun, ay_ad, saat = parcalar[:3]
                    ay = aylar.get(ay_ad)
                    yil = datetime.now().year
                    tarih_iso = f"{yil}-{ay}-{int(gun):02d}T{saat}:00"
                else:
                    tarih_iso = tarih_text
            except Exception:
                tarih_iso = tarih_text
        else:
            # 2️⃣ Alternatif: tüm article metni içinde regex ile tarih ara
            article_text = article.get_text(separator=" ", strip=True).lower()
            match = re.search(r"(\d{1,2}) (ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık) (\d{2}:\d{2})", article_text)
            if match:
                gun, ay_ad, saat = match.groups()
                ay = aylar.get(ay_ad)
                yil = datetime.now().year
                tarih_iso = f"{yil}-{ay}-{int(gun):02d}T{saat}:00"

        filtreli_yorumlar.append({
            "id": str(uuid.uuid4()),
            "yorum": yorum,
            "tarih": tarih_iso,
            "kaynak": "sikayetvar"
        })

    except Exception as e:
        print(f"⚠️ Hata: {e}")
        continue

# JSON'a yaz
with open("yorumlar_tarihli_filtreli.json", "w", encoding="utf-8") as dosya:
    json.dump(filtreli_yorumlar, dosya, ensure_ascii=False, indent=2)

print(f"✅ {len(filtreli_yorumlar)} yorum bulundu ve kaydedildi.")
