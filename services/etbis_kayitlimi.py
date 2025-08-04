import json
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


def etbis_kayit_kontrol(girdi: str) -> str:
    girdi = girdi.replace(" ", "")  # boşlukları sil
    if not girdi.startswith("http"):
        site_url = f"https://www.{girdi}"
    else:
        site_url = girdi

    base_url = "https://etbis.ticaret.gov.tr/tr/Home/SearchSite?url="
    tam_url = base_url + site_url

    options = Options()
    #options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service("C:/Users/gedik/tools/chromedriver-win64/chromedriver.exe"),
        options=options
    )

    try:
        driver.get(tam_url)
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1.5)
        tr_satirlari = driver.find_elements(By.XPATH, "//table//tr")
        if not tr_satirlari:
            return f"{site_url} E-Ticaret Bilgi Sistemine sisteminde kayıtlı değildir."

        try:
            img = driver.find_element(By.XPATH, "//table//tr/td[3]/img")
            src = img.get_attribute("src")
            if "unverified.png" in src:
                mobil_durum = "Mobil uygulaması YOK."
            elif "verified.png" in src:
                mobil_durum = "Mobil uygulaması VAR."
            else:
                mobil_durum = "Mobil uygulama durumu belirlenemedi."
        except:
            return f"{site_url} E-Ticaret Bilgi Sistemine sisteminde kayıtlı değildir."

        return f"{site_url} E-Ticaret Bilgi Sistemine sisteminde kayıtlıdır. {mobil_durum}"

    except Exception as e:
        return f"{site_url} için kontrol sırasında bir hata oluştu: {str(e)}"
    finally:
        driver.quit()


def yorumu_jsona_ekle(yorum: str, json_dosya_yolu: str = "yorumlar_tarihli_filtreli.json"):
    try:
        with open(json_dosya_yolu, "r", encoding="utf-8") as f:
            mevcut_yorumlar = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        mevcut_yorumlar = []

    yeni_yorum = {
        "id": str(uuid.uuid4()),
        "yorum": yorum,
        "kaynak": "E-Ticaret Bilgi Sistemi"
    }

    mevcut_yorumlar.append(yeni_yorum)

    with open(json_dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(mevcut_yorumlar, f, ensure_ascii=False, indent=2)

