from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_sikayetvar(site_name: str, max_entries: int = 5) -> list[str]:
    url_site_name = site_name.replace(".", "-")
    url = f"https://www.sikayetvar.com/{url_site_name}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service("C:/Users/gedik/tools/chromedriver-win64/chromedriver.exe"),
        options=options
    )
    driver.get(url)

    try:
        # En fazla 10 saniye boyunca yorum elemanlarının gelmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.card-text"))
        )
    except Exception as e:
        print(f"Yorumlar yüklenmedi veya hata oluştu: {e}")
    
    # Sayfa içeriğini çek
    soup = BeautifulSoup(driver.page_source, "html.parser")
    entries = soup.find_all("p", class_="card-text")
    yorumlar = [entry.get_text(strip=True) for entry in entries[:max_entries]]

    # Yorumlar boşsa HTML’yi kaydet
    if not yorumlar:
        with open("sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    driver.quit()
    return yorumlar
