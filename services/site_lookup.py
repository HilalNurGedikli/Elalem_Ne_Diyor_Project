from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess
import time
import sys
import json

def scrape_sikayetvar(site_name: str) -> list[dict]:
    url_site_name = site_name.replace(".", "-")
    url = f"https://www.sikayetvar.com/{url_site_name}"

    options = Options()
    # options.add_argument("--headless")  # İstersen aktif et
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service("C:/Users/gedik/tools/chromedriver-win64/chromedriver.exe"),
        options=options
    )
    driver.get(url)

    # Sayfa biraz yüklensin diye aşağı kaydır
    for _ in range(2):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1.5)

    # Sayfayı kaydet
    with open("sayfa.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("HTML sayfası kaydedildi: sayfa.html")

    # yorumlari_cek.py dosyasını çalıştır
    print("Yorumları işleyen Python dosyası çalıştırılıyor...")
    subprocess.run([sys.executable, "yorumlari_cek.py"], check=True)

    driver.quit()


