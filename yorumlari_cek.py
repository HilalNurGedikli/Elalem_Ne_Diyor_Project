from bs4 import BeautifulSoup
import json

with open("sayfa.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# JSON scriptlerini bul
json_scripts = soup.find_all("script", type="application/ld+json")
print(f"{len(json_scripts)} tane JSON script bulundu.")

for i, script in enumerate(json_scripts):
    print(f"\n--- SCRIPT {i+1} ---")
    try:
        print(script.string[:500])  # İlk 500 karakteri göster
    except:
        print("Script okunamadı.")
