from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def etbis_kayit_kontrol(girdi: str) -> str:
    if not girdi.startswith("http"):
        site_url = f"https://www.{girdi}"
    else:
        site_url = girdi

    base_url = "https://etbis.ticaret.gov.tr/tr/Home/SearchSite?url="
    tam_url = base_url + site_url

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service("C:/Users/gedik/tools/chromedriver-win64/chromedriver.exe"),
        options=options
    )

    try:
        driver.get(tam_url)

        # Sayfada en az bir <tr> varsa, kayıtlıdır
        tr_satirlari = driver.find_elements(By.XPATH, "//table//tr")
        if not tr_satirlari:
            return f"{site_url} ETBİS sisteminde kayıtlı değildir."

        # td[3]/img üzerinden mobil durumu kontrolü
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
            return f"{site_url} ETBİS sisteminde kayıtlı değildir."

        return f"{site_url} ETBİS sisteminde kayıtlıdır. {mobil_durum}"

    except Exception as e:
        return f"{site_url} için kontrol sırasında bir hata oluştu: {str(e)}"
    finally:
        driver.quit()


if __name__ == "__main__":
    site = "https://www.bershka.com"
    sonuc = etbis_kayit_kontrol(site)
    print(sonuc)
