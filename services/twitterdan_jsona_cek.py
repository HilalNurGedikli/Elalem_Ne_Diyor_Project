import requests
import json
from datetime import datetime
from pathlib import Path

def twitter_yorum_ekle(query: str, max_results: int = 10, json_dosya: str = "yorumlar_tarihli_filtreli.json"):
    """Twitter'dan belirtilen sorguya göre yorumları alıp JSON dosyasına ekler."""

    bearer_token = "AAAAAAAAAAAAAAAAAAAAANqW3QEAAAAAYo6pM%2B8%2FJMevEoAWDLyb2LivW40%3DhUYPxY0yiiLOX0pyGKBKnnMDHRXx9sN6OyDgQNFcIF8aFsKPo1"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = (
        f"https://api.twitter.com/2/tweets/search/recent"
        f"?query={query}&max_results={max_results}&tweet.fields=created_at,lang"
    )

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
