import requests

def fetch_disaster_news():
    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "disaster OR flood OR earthquake OR fire OR accident",
        "mode": "ArtList",
        "format": "json",
        "maxrecords": 10,
        "sort": "HybridRel"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        articles = []

        for item in data.get("articles", []):
            articles.append({
                "title": item.get("title", "No title"),
                "source": item.get("sourceCountry", "Unknown"),
                "url": item.get("url", "")
            })

        return articles

    except Exception:
        return []