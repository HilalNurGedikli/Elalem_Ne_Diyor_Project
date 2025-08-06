import requests
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def twitter_yorum_ekle(query: str, max_results: int = 50, json_dosya: str = "yorumlar_tarihli_filtreli.json"):
    """Twitter'dan belirtilen sorguya göre yorumları alıp JSON dosyasına ekler."""

    # Environment değişkenlerinden Twitter Bearer Token'ı al
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token:
        print("❌ TWITTER_BEARER_TOKEN environment değişkeni bulunamadı!")
        print("🔧 Lütfen .env dosyasında TWITTER_BEARER_TOKEN değişkenini ayarlayın")
        return []
    
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = (
        f"https://api.twitter.com/2/tweets/search/recent"
        f"?query={query}&max_results={max_results}&tweet.fields=created_at,lang"
    )

    print(f"🐦 Twitter API isteği gönderiliyor: {query}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[HATA] Twitter API isteği başarısız oldu. Kod: {response.status_code}")
        return

    data = response.json()
    tweet_yorumlar = []
    for i, tweet in enumerate(data.get("data", []), 1):
        tweet_yorumlar.append({
            "id": f"tw-{i}",
            "yorum": tweet["text"],
            "tarihler": [tweet["created_at"][:10]],
            "kaynak": "twitter"
        })

    # Mevcut JSON dosyasını yükle
    if Path(json_dosya).exists():
        with open(json_dosya, "r", encoding="utf-8") as f:
            mevcut_yorumlar = json.load(f)
    else:
        mevcut_yorumlar = []

    mevcut_yorumlar.extend(tweet_yorumlar)

    # JSON’a geri yaz
    with open(json_dosya, "w", encoding="utf-8") as f:
        json.dump(mevcut_yorumlar, f, ensure_ascii=False, indent=2)

    print(f"{len(tweet_yorumlar)} tweet eklendi.")

# Örnek kullanım:
# twitter_yorum_ekle("ceylan otantik")
