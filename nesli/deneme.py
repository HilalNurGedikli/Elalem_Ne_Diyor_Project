import requests

bearer_token = "AAAAAAAAAAAAAAAAAAAAAAz53AEAAAAAVDJhfP%2FNGjTlUxg8SZ2%2BaRmlsRM%3Dapnkbo0p7mZuVXesRCxnvpp6bCy3k7EdLa1q1Q9CZDsDfZMEum"
headers = {"Authorization": f"Bearer {bearer_token}"}
query = "ceylan otantik"

url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=created_at,lang"

response = requests.get(url, headers=headers)
print("Status:", response.status_code)
print("Raw JSON:", response.json())
tweets = response.json()["data"]

for t in tweets:
    print(t["text"])
