import hashlib
import os
import random
from datetime import datetime, timedelta

import feedparser
import requests

from data.data_collector import detect_region, rss_feeds


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def generate_post_id(content: str, source: str) -> str:
    return hashlib.md5(f"{source}:{content}".encode("utf-8")).hexdigest()


def _post(platform, source, content, region=None, engagement=0, url="", timestamp=None):
    return {
        "post_id": generate_post_id(content, source),
        "platform": platform,
        "source": source,
        "region": region or detect_region(content),
        "content": content,
        "timestamp": timestamp or datetime.utcnow().isoformat(),
        "engagement": int(engagement or 0),
        "url": url,
    }


def _mark_backup(posts, reason):
    return [{**post, "backup": True, "backup_reason": reason} for post in posts]


def _with_real_marker(posts):
    return [{**post, "backup": False, "backup_reason": ""} for post in posts]


# -------------------------
# SIMULATION FUNCTIONS
# -------------------------

def simulate_rss_sources(limit_per_feed=10):
    """Simulation des sources RSS avec données fictives mais réalistes"""
    regions = ["Tunis", "Sfax", "Gabes", "Jendouba", "Sousse", "Kairouan"]
    sources = list(rss_feeds.keys())
    posts = []
    
    for source in sources:
        for i in range(random.randint(1, limit_per_feed)):
            region = random.choice(regions)
            content_options = [
                f"Actualité {region}: développement urbain en cours",
                f"Événement culturel à {region} ce weekend",
                f"Politique locale: réunion municipale à {region}",
                f"Sport: victoire de l'équipe de {region}",
                f"Économie: nouvelle entreprise s'installe à {region}",
                f"Éducation: ouverture d'une nouvelle école à {region}",
                f"Santé: campagne de vaccination à {region}",
                f"Environnement: projet écologique à {region}",
            ]
            content = random.choice(content_options)
            engagement = random.randint(10, 100)
            timestamp = (datetime.utcnow() - timedelta(hours=random.randint(0, 24))).isoformat()
            
            posts.append(
                _post(
                    "RSS",
                    source,
                    content,
                    region=region,
                    engagement=engagement,
                    url=f"https://example.com/rss/{source.lower().replace(' ', '-')}/{i}",
                    timestamp=timestamp,
                )
            )
    return posts


def simulate_google_trends_sources(keywords=None):
    """Simulation des tendances Google avec données fictives"""
    keywords = keywords or ["Tunisie", "Tunis", "Sfax", "Gabes", "Jendouba"]
    regions = ["Tunis", "Sfax", "Gabes", "Jendouba", "Sousse", "Kairouan"]
    posts = []
    
    for keyword in keywords:
        for i in range(random.randint(1, 3)):
            region = random.choice(regions)
            trend_options = [
                f"Hausse des recherches: {keyword} élections",
                f"Recherches en hausse: {keyword} météo",
                f"Tendance: {keyword} actualités politiques",
                f"Pic de recherches: {keyword} événements culturels",
                f"Intérêt croissant: {keyword} économie locale",
                f"Trending: {keyword} sports régionaux",
            ]
            content = random.choice(trend_options)
            engagement = random.randint(40, 90)
            
            posts.append(
                _post(
                    "Google Trends",
                    "Google Trends TN",
                    content,
                    region=region,
                    engagement=engagement,
                )
            )
    return posts


def simulate_youtube_sources(query="Tunisie actualite OR trend", max_results=10):
    """Simulation des vidéos YouTube avec données fictives"""
    regions = ["Tunis", "Sfax", "Gabes", "Jendouba", "Sousse", "Kairouan"]
    channels = ["Tunisia News", "Local TV", "Citizen Reporter", "Culture TN", "Sports Tunisia"]
    posts = []
    
    for i in range(random.randint(1, max_results)):
        region = random.choice(regions)
        channel = random.choice(channels)
        video_options = [
            f"Actualités {region}: résumé de la semaine",
            f"Reportage: vie quotidienne à {region}",
            f"Débat politique en direct de {region}",
            f"Événement culturel à {region}",
            f"Sport régional: match à {region}",
            f"Tourisme: découvrir {region}",
            f"Interview: personnalités de {region}",
            f"Trend viral originaire de {region}",
        ]
        title = random.choice(video_options)
        engagement = random.randint(50, 95)
        video_id = f"sim_{hashlib.md5(title.encode()).hexdigest()[:8]}"
        timestamp = (datetime.utcnow() - timedelta(hours=random.randint(0, 48))).isoformat()
        
        posts.append(
            _post(
                "YouTube",
                channel,
                title,
                region=region,
                engagement=engagement,
                url=f"https://www.youtube.com/watch?v={video_id}",
                timestamp=timestamp,
            )
        )
    return posts


def collect_all_sources_simulation():
    """Collecte simulée de toutes les sources (mode backup/simulation)"""
    posts = []
    posts.extend(simulate_rss_sources())
    posts.extend(simulate_google_trends_sources())
    posts.extend(simulate_youtube_sources())
    return posts


# -------------------------
# REAL FUNCTIONS
# -------------------------

def fetch_rss_sources(limit_per_feed=10, use_backup=True):
    posts = []
    headers = {"User-Agent": "TnassnissaDashboard/1.0"}
    for source, url in rss_feeds.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            for entry in feed.entries[:limit_per_feed]:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                posts.append(
                    _post(
                        "RSS",
                        source,
                        title,
                        url=entry.get("link", ""),
                        timestamp=entry.get("published", "") or None,
                    )
                )
        except Exception as exc:
            print(f"RSS skipped for {source}: {exc}")
    if posts:
        return _with_real_marker(posts)
    if use_backup:
        print("RSS simulation backup used: no RSS posts collected")
        return _mark_backup(simulate_rss_sources(limit_per_feed=3), "rss_unavailable")
    return []


def fetch_google_trends_sources(keywords=None, use_backup=True):
    keywords = keywords or ["Tunisie", "Tunis", "Sfax", "Gabes", "Jendouba"]
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="fr-TN", tz=60)
        pytrends.build_payload(keywords, geo="TN", timeframe="now 7-d")
        related = pytrends.related_queries()
        posts = []
        for keyword, payload in related.items():
            top = payload.get("top") if payload else None
            if top is None:
                continue
            for row in top.head(5).to_dict("records"):
                query = row.get("query", keyword)
                value = row.get("value", 0)
                posts.append(
                    _post(
                        "Google Trends",
                        "Google Trends TN",
                        f"Hausse des recherches: {query}",
                        engagement=value,
                    )
                )
        if posts:
            return _with_real_marker(posts)
        if use_backup:
            print("Google Trends simulation backup used: no related queries returned")
            return _mark_backup(simulate_google_trends_sources(keywords), "google_trends_empty")
        return []
    except Exception as exc:
        print(f"Google Trends fallback used: {exc}")
        if use_backup:
            return _mark_backup(simulate_google_trends_sources(keywords), "google_trends_unavailable")
        return []


def fetch_youtube_sources(query="Tunisie actualite OR trend", max_results=10, use_backup=True):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("YouTube simulation backup used: missing YOUTUBE_API_KEY")
        return _mark_backup(simulate_youtube_sources(query, max_results=3), "youtube_api_key_missing") if use_backup else []

    try:
        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "regionCode": "TN",
                "maxResults": max_results,
                "order": "date",
                "key": api_key,
            },
            timeout=10,
        )
        response.raise_for_status()
        posts = []
        for item in response.json().get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId", "")
            title = snippet.get("title", "").strip()
            if not title:
                continue
            posts.append(
                _post(
                    "YouTube",
                    snippet.get("channelTitle", "YouTube"),
                    title,
                    engagement=50,
                    url=f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
                    timestamp=snippet.get("publishedAt"),
                )
            )
        if posts:
            return _with_real_marker(posts)
        if use_backup:
            print("YouTube simulation backup used: no videos returned")
            return _mark_backup(simulate_youtube_sources(query, max_results=3), "youtube_empty")
        return []
    except Exception as exc:
        print(f"YouTube fallback used: {exc}")
        if use_backup:
            return _mark_backup(simulate_youtube_sources(query, max_results=3), "youtube_unavailable")
        return []


def collect_all_sources(use_backup=True):
    """Collecte réelle de toutes les sources"""
    posts = []
    posts.extend(fetch_rss_sources(use_backup=use_backup))
    posts.extend(fetch_google_trends_sources(use_backup=use_backup))
    posts.extend(fetch_youtube_sources(use_backup=use_backup))
    if not posts and use_backup:
        print("Full source simulation backup used: every collector returned empty")
        return _mark_backup(collect_all_sources_simulation(), "all_sources_empty")
    return posts
