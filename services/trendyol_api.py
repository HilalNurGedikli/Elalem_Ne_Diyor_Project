from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import re


def get_store_id_from_search(store_name):
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.trendyol.com/")
    time.sleep(2)

    search_input = driver.find_element(
        By.CSS_SELECTOR, "input[data-testid='suggestion']"
    )
    search_input.send_keys(store_name)
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)

    # İlk bulunan mağaza linkini yakala
    store_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/magaza/']")
    if not store_links:
        print("❌ Mağaza bulunamadı.")
        driver.quit()
        return None

    store_url = store_links[0].get_attribute("href")
    driver.quit()

    match = re.search(r"-m-(\d+)", store_url)
    if match:
        return int(match.group(1)), store_url
    else:
        return None, store_url


# Örnek kullanım (sadece doğrudan çalıştırıldığında)
if __name__ == "__main__":
    store_id, url = get_store_id_from_search("Epify")
    if store_id and url:
        print("✅ Store ID:", store_id)
        print("🔗 Mağaza URL:", url)
    else:
        print("❌ Store bulunamadı")

def scrape_trendyol(site_name: str) -> list:
    """Trendyol scraping fonksiyonu - API entegrasyonu için"""
    try:
        # Burada Trendyol scraping implementasyonu olacak
        return []
    except Exception as e:
        print(f"Trendyol scraping hatası: {e}")
        return []
