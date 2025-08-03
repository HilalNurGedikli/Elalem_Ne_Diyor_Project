from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys
import json
import os

from get_param import Paths as path

JSON_PATH = path.json_path
TXT_PATH = path.txt_path


def scrape_eksi(baslik: str, max_pages: int = 3) -> None:
    url_baslik = baslik.lower().replace(" ", "%20")
    url = f"https://eksisozluk.com/{url_baslik}"

    # Dosya adlarını hazırla
    json_filename = f"{JSON_PATH}/_{url_baslik}_eksi_entryler.json"
    txt_filename = f"{TXT_PATH}/_{url_baslik}_eksi_entryler.txt"

    # JSON dosyasını baştan boş bir liste ile başlat
    with open(json_filename, "w", encoding="utf-8") as f_json:
        json.dump([], f_json)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    current_page = 1
    entry_count = 0

    while True:
        current_url = driver.current_url
        print(f"\n🔗 URL: {current_url}")
        print(f"🟦 Sayfa {current_page} işleniyor...")

        # Aşağı kaydır (içerik yüklemesi için)
        for _ in range(2):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)

        entries = driver.find_elements(By.CSS_SELECTOR, ".content")
        print(f"{len(entries)} entry bulundu.")

        if len(entries) == 0:
            print("🟨 Entry bulunamadı, işlem durduruluyor.")
            break

        new_entries = []
        with open(txt_filename, "a", encoding="utf-8") as f_txt:
            for i, entry in enumerate(entries, 1):
                text = entry.text.strip()
                entry_count += 1
                print(f"{entry_count}. {text}")
                f_txt.write(f"{entry_count}. {text}\n\n")
                new_entries.append(text)

        # JSON'a ekle
        with open(json_filename, "r+", encoding="utf-8") as f_json:
            existing = json.load(f_json)
            f_json.seek(0)
            json.dump(existing + new_entries, f_json, ensure_ascii=False, indent=2)
            f_json.truncate()

        if current_page >= max_pages:
            print("🟥 Maksimum sayfa sınırına ulaşıldı.")
            break

        try:
            current_page += 1
            parca = current_url.split("?")[0]
            next_url = f"{parca}?p={current_page}"
            print(f"➡️ Next URL: {next_url}")
            driver.get(next_url)
            time.sleep(2)
        except Exception as e:
            print(f"❌ Sonraki sayfaya geçilemedi: {e}")
            break

    driver.quit()
    print("✅ Her sayfa çekildikçe veriler yazıldı ve işlem tamamlandı.")


if __name__ == "__main__":
    # Klasörler yoksa oluştur
    os.makedirs(JSON_PATH, exist_ok=True)
    os.makedirs(TXT_PATH, exist_ok=True)

    scrape_eksi("selcuk bayraktar", max_pages=5)
