import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

JSON_PATH = "veriler/json"
TXT_PATH = "veriler/txt"


def get_instagram_stats(username):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")  # İngilizce dilde açılmasını sağlar

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"https://www.instagram.com/{username}/"
        driver.get(url)
        time.sleep(5)

        stats = driver.find_elements(By.CSS_SELECTOR, "header section ul li")

        if len(stats) >= 3:
            post_text = stats[0].text.split("\n")[0]
            followers_text = stats[1].text.split("\n")[0]
            following_text = stats[2].text.split("\n")[0]

            data = {
                "username": username,
                "posts": post_text,
                "followers": followers_text,
                "following": following_text,
                "url": url,
            }

            # 🔹 JSON olarak kaydet
            with open(
                f"{JSON_PATH}/{username}_insta_stats.json", "w", encoding="utf-8"
            ) as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            # 🔹 TXT olarak kaydet
            with open(
                f"{TXT_PATH}/{username}insta_stats.txt", "w", encoding="utf-8"
            ) as txt_file:
                txt_file.write(f"👤 Kullanıcı: {username}\n")
                txt_file.write(f"📸 Gönderi sayısı: {post_text}\n")
                txt_file.write(f"👥 Takipçi sayısı: {followers_text}\n")
                txt_file.write(f"➡️ Takip edilen: {following_text}\n")
                txt_file.write(f"🔗 Profil: {url}\n")

            print("✅ Veriler başarıyla kaydedildi.")
        else:
            print("❌ Veriler alınamadı. Sayfa yapısı değişmiş olabilir.")
    finally:
        driver.quit()


if __name__ == "__main__":
    get_instagram_stats("batoddy_")
