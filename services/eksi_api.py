from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import uuid
import sys
import json
import os

from services.get_param import Paths as path
TXT_PATH = path.txt_path

def scrape_eksi(baslik: str, max_pages: int = 3) -> None:
    os.makedirs(TXT_PATH, exist_ok=True)

    url_baslik = baslik.lower().replace(" ", "%20")
    url = f"https://eksisozluk.com/{url_baslik}"
    json_filename = "yorumlar_tarihli_filtreli.json"
    txt_filename = f"{TXT_PATH}/_{url_baslik}_eksi_entryler.txt"

    options = Options()
    options.add_argument("--headless")  # Browser penceresi açılmayacak
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")

    # ChromeDriver path'ini doğru şekilde ayarla
    try:
        # Önce yerel ChromeDriver'ı dene
        driver = webdriver.Chrome(
            service=Service(r"c:\Users\gzmns\onedrivefake\Masaüstü\elalem\Elalem_Ne_Diyor_Project\services\chromedriver.exe"),
            options=options
        )
        print("✅ Yerel ChromeDriver kullanılıyor")
    except Exception as e:
        print(f"⚠️ Yerel ChromeDriver çalışmadı: {e}")
        try:
            # WebDriverManager ile dene
            from webdriver_manager.chrome import ChromeDriverManager
            
            # Cache'i temizle ve yeniden indir
            wdm_path = ChromeDriverManager().install()
            print(f"📥 WebDriverManager path: {wdm_path}")
            
            # WebDriverManager bazen yanlış dosyayı döndürür, doğru exe dosyasını bulalım
            if "THIRD_PARTY_NOTICES" in wdm_path:
                # WebDriverManager yanlış dosya döndürdü, doğru chromedriver.exe'yi bulalım
                driver_dir = os.path.dirname(wdm_path)
                chromedriver_exe = os.path.join(driver_dir, "chromedriver.exe")
                if os.path.exists(chromedriver_exe):
                    wdm_path = chromedriver_exe
                    print(f"🔧 Doğru driver bulundu: {wdm_path}")
                else:
                    # chromedriver-win32 klasörünü kontrol et
                    chromedriver_exe = os.path.join(driver_dir, "chromedriver-win32", "chromedriver.exe")
                    if os.path.exists(chromedriver_exe):
                        wdm_path = chromedriver_exe
                        print(f"🔧 Win32 klasöründe driver bulundu: {wdm_path}")
            
            # Dosyanın var olup olmadığını kontrol et
            if os.path.exists(wdm_path) and wdm_path.endswith('.exe'):
                driver = webdriver.Chrome(service=Service(wdm_path), options=options)
                print("✅ WebDriverManager ChromeDriver kullanılıyor")
            else:
                raise Exception(f"WebDriverManager exe dosyası bulunamadı: {wdm_path}")
                
        except Exception as e2:
            print(f"❌ WebDriverManager de çalışmadı: {e2}")
            # Son çare: system PATH'teki chromedriver'ı kullan
            try:
                driver = webdriver.Chrome(options=options)
                print("✅ System PATH ChromeDriver kullanılıyor")
            except Exception as e3:
                raise Exception(f"Hiçbir ChromeDriver çalışmadı: {e3}")
    
    driver.get(url)
    time.sleep(3)

    current_page = 1
    entry_count = 0
    all_new_entries = []

    while True:
        current_url = driver.current_url
        print(f"\n🔗 URL: {current_url}")
        print(f"🟦 Sayfa {current_page} işleniyor...")

        for _ in range(2):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1.5)
        entry_blocks = driver.find_elements(By.CSS_SELECTOR, "li[id^='entry']")
        print(entry_blocks)
        print(f"{len(entry_blocks)} entry bulundu.")

        if not entry_blocks:
            print("🟨 Entry bulunamadı, işlem durduruluyor.")
            break

        with open(txt_filename, "a", encoding="utf-8") as f_txt:
        
            for entry_block in entry_blocks:
                try:
                    text_element = entry_block.find_element(By.CSS_SELECTOR, ".content")
                    date_element = entry_block.find_element(By.CSS_SELECTOR, "a.entry-date")

                    text = text_element.text.strip()
                    tarih = date_element.text.strip()

                    if not text:
                        continue

                    entry_count += 1
                    print(f"{entry_count}. ({tarih}) {text}")
                    f_txt.write(f"{entry_count}. ({tarih}) {text}\n\n")

                    all_new_entries.append({
                        "id": str(uuid.uuid4()),
                        "yorum": text,
                        "tarih": tarih,
                        "kaynak": "eksi"
                    })
                except Exception as e:
                    print(f"⚠️ Hata (entry atlanıyor): {e}")
                    continue


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

    # JSON'a yaz
    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf-8") as f_json:
            existing = json.load(f_json)
    else:
        existing = []

    existing.extend(all_new_entries)

    with open(json_filename, "w", encoding="utf-8") as f_json:
        json.dump(existing, f_json, ensure_ascii=False, indent=2)

    print("✅ Her sayfa çekildikçe veriler yazıldı ve işlem tamamlandı.")