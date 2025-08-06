from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import sys
import json
import re
import os
from bs4 import BeautifulSoup
import uuid
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def scrape_sikayetvar(site_name: str) -> list[dict]:
    """Şikayetvar.com'dan yorumları çek ve işle - HTML dosyası kaydetmeden"""
    url_site_name = site_name.replace(".", "-")
    url = f"https://www.sikayetvar.com/{url_site_name}"

    # Anahtar kelimeler
    anahtar_kelimeler = [
        "şikayet", "şikayetçi", "memnun değilim", "pişman", "iade", "ret", "reddedildi",
        "yırtıldı", "kırıldı", "soyuldu", "çatladı", "şikayetim", "kalitesiz", "hüsran",
        "yanıltıcı", "bozuldu", "incelendi", "olumsuz", "reddi", "değişim yapılmadı",
        "memnun", "teşekkür", "çok beğendim", "sorunsuz", "iyi hizmet", "kaliteli",
        "hızlı teslimat", "olumlu", "tavsiye ederim", "güzel", "iyi ki", "harika", "çok güzel",
        "beğendim", "mükemmel", "tatmin oldum", "şahane", "kusursuz"
    ]
    
    # Türkçe aylar sözlüğü
    aylar = {
        "ocak": "01", "şubat": "02", "mart": "03", "nisan": "04", "mayıs": "05", "haziran": "06",
        "temmuz": "07", "ağustos": "08", "eylül": "09", "ekim": "10", "kasım": "11", "aralık": "12"
    }

    options = Options()
    options.add_argument("--headless")  # Browser penceresi açılmayacak
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # ChromeDriver path'ini environment variable'dan al
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH', './services/chromedriver.exe')
    fallback_path = os.getenv('CHROMEDRIVER_FALLBACK_PATH', 'chromedriver')
    
    try:
        # Önce birincil path'i dene
        driver = webdriver.Chrome(
            service=Service(chromedriver_path),
            options=options
        )
    except Exception as e:
        print(f"⚠️ Birincil ChromeDriver çalışmadı ({chromedriver_path}): {e}")
        try:
            # Fallback path'i dene
            driver = webdriver.Chrome(
                service=Service(fallback_path),
                options=options
            )
        except Exception as e2:
            print(f"⚠️ Fallback ChromeDriver çalışmadı ({fallback_path}): {e2}")
            # WebDriverManager ile dene
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
    
    try:
        driver.get(url)

        # Sayfa biraz yüklensin diye aşağı kaydır
        for _ in range(2):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1.5)

        # HTML içeriğini doğrudan işle (dosyaya kaydetmeden)
        html_content = driver.page_source
        print("✅ Sayfa içeriği alındı (bellekte işleniyor)")
        
        # BeautifulSoup ile işle
        soup = BeautifulSoup(html_content, "html.parser")
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

                # Div içinden tarihi çekmeye çalış
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

                filtreli_yorumlar.append({
                    "id": str(uuid.uuid4()),
                    "yorum": yorum,
                    "tarih": tarih_iso,
                    "kaynak": "sikayetvar",
                    "site": site_name
                })

            except Exception as e:
                print(f"⚠️ Yorum işleme hatası: {e}")
                continue

        print(f"✅ {len(filtreli_yorumlar)} yorum bulundu ve işlendi")
        return filtreli_yorumlar

    finally:
        driver.quit()


# Eski fonksiyon kaldırıldı - artık direkt bellekte işliyoruz


