import feedparser
from ..config import YOUTUBE_API_KEY

FEEDS = {
    "sports": [
        "https://www.mosaiquefm.net/fr/rss/sport",
        "https://www.businessnews.com.tn/rss/sport"
    ],
    "fashion": [
        "https://www.mosaiquefm.net/fr/rss/mode",
        "https://www.tunisie.co/rss/mode"
    ],
    "tech": [
        "https://www.mosaiquefm.net/fr/rss/technologie",
        "https://www.webdo.tn/feed/"
    ],
    "general": [
        "https://www.mosaiquefm.net/fr/rss/national",
        "https://www.tuniscope.com/rss"
    ]
}

def fetch_rss(interest):
    articles = []
    for url in FEEDS.get(interest, FEEDS["general"]):
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": url.split("/")[2],
                "domain": interest
            })
    return articles

def fetch_google_trends(interest):
    # Simulation (pytrends peut être ajouté plus tard)
    return [{
        "title": f"Tendance Google : {interest}",
        "summary": f"Le sujet '{interest}' gagne +35% d'intérêt en Tunisie.",
        "link": "https://trends.google.com",
        "published": "",
        "source": "Google Trends",
        "domain": interest
    }]

def fetch_youtube(interest):
    if not YOUTUBE_API_KEY:
        return []
    # Optionnel : intégration réelle
    return []

def get_news_by_interest(interest):
    articles = fetch_rss(interest)
    articles += fetch_google_trends(interest)
    articles += fetch_youtube(interest)
    return articles