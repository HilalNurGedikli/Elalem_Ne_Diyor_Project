from bs4 import BeautifulSoup
import re
import json

# Anahtar kelimeler
anahtar_kelimeler = [
    # Olumsuz ifadeler
    "şikayet", "şikayetçi", "memnun değilim", "pişman", "iade", "ret", "reddedildi",
    "yırtıldı", "kırıldı", "soyuldu", "çatladı", "şikayetim", "kalitesiz", "hüsran",
    "yanıltıcı", "bozuldu", "incelendi", "olumsuz", "reddi", "değişim yapılmadı",

    # Olumlu ifadeler
    "memnun", "teşekkür", "çok beğendim", "sorunsuz", "iyi hizmet", "kaliteli",
    "hızlı teslimat", "olumlu", "tavsiye ederim", "güzel", "iyi ki", "harika", "çok güzel",
    "beğendim", "mükemmel", "tatmin oldum", "şahane", "kusursuz"
]


# Tarih deseni: 24.03.2025 veya 03/04/2025 gibi
tarih_deseni = r"\d{4}[-]\d{2}[-]\d{2}"

# HTML oku
with open("sayfa.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
paragraflar = soup.find_all("p")

# Yorumları topla
filtreli_yorumlar = []

for i, p in enumerate(paragraflar, 1):
    metin = p.get_text(strip=True).lower()
    if any(kelime in metin for kelime in anahtar_kelimeler):
        tarihler = re.findall(tarih_deseni, metin)
        filtreli_yorumlar.append({
            "id": i,
            "yorum": metin,
            "tarihler": tarihler
        })

# JSON'a kaydet
with open("yorumlar_tarihli_filtreli.json", "w", encoding="utf-8") as dosya:
    json.dump(filtreli_yorumlar, dosya, ensure_ascii=False, indent=2)

print(f"{len(filtreli_yorumlar)} yorum bulundu ve filtrelenmiş şekilde kaydedildi.")
