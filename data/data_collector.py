import sqlite3
import feedparser
import hashlib
import os
import requests
from datetime import datetime

# Facebook scraping optionnel
FACEBOOK_AVAILABLE = True
try:
    from facebook_scraper import get_posts
except ImportError:
    FACEBOOK_AVAILABLE = False


DB_NAME = os.path.join(os.path.dirname(__file__), "raw_data.db")

# -----------------------------
# RSS Tunisiens réels
# -----------------------------
rss_feeds = {
    "LaPresse": "https://www.lapresse.tn/feed/",
    "TunisieFocus": "https://www.tunisiefocus.com/feed/",
    "Babnet": "https://www.babnet.net/feed.php",
    "Realites": "https://www.realites.com.tn/fr/feed/",
    "AfricanManager": "https://africanmanager.com/feed/",
    "Leaders": "https://www.leaders.com.tn/rss"
}

# -----------------------------
# Pages Facebook ciblées
# -----------------------------
facebook_pages = {
    "Tunis": "alert.tunisie",
    "Sfax": "RadioDiwanFM",
    "Gabès": "Gabes.Ali5baria",
    "Jendouba": "newsjendouba24"
}


# -----------------------------
# Base SQLite
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Posts (
        post_id TEXT PRIMARY KEY,
        platform TEXT,
        source TEXT,
        region TEXT,
        content TEXT,
        timestamp TEXT,
        engagement INTEGER,
        url TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Base de données créée avec succès")


# -----------------------------
# ID unique
# -----------------------------
def generate_post_id(content):
    return hashlib.md5(content.encode("utf-8")).hexdigest()


# -----------------------------
# Détection régionale
# -----------------------------
def detect_region(text):
    region_keywords = {
        "Tunis": [
            "tunis", "tunisie", "la marsa",
            "ariana", "ben arous", "manouba",
            "carthage", "bardo"
        ],
        "Sfax": [
            "sfax", "sakiet ezzit",
            "sakiet eddaier", "kerkennah",
            "thyna"
        ],
        "Gabès": [
            "gabès", "gabes",
            "el hamma", "matmata", "mareth"
        ],
        "Jendouba": [
            "jendouba", "ain draham",
            "tabarka", "bousalem"
        ]
    }

    text_lower = text.lower()

    for region, keywords in region_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return region

    return "Autre"


# -----------------------------
# Collecte RSS
# -----------------------------
def fetch_rss():
    posts = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for source, url in rss_feeds.items():
        print(f"\n📡 Collecte RSS depuis {source}...")

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10,
                allow_redirects=True
            )

            print("Status:", response.status_code)

            feed = feedparser.parse(response.content)
            print("Nombre entries:", len(feed.entries))

            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                published = entry.get("published", "")

                if not title:
                    continue

                region = detect_region(title)

                post = {
                    "post_id": generate_post_id(title + source),
                    "platform": "News",
                    "source": source,
                    "region": region,
                    "content": title,
                    "timestamp": published,
                    "engagement": 0,
                    "url": link
                }

                posts.append(post)

        except Exception as e:
            print(f"❌ Erreur RSS avec {source}: {e}")

    return posts


# -----------------------------
# Facebook réel (tentative)
# -----------------------------
def fetch_facebook_posts():
    posts = []

    if not FACEBOOK_AVAILABLE:
        print("\n⚠️ facebook_scraper non disponible — passage au fallback simulé")
        return posts

    for region, page_name in facebook_pages.items():
        print(f"\n📘 Collecte Facebook réelle depuis {page_name} ({region})...")

        try:
            count = 0

            for fb_post in get_posts(
                page_name,
                pages=5,
                options={
                    "comments": False,
                    "allow_extra_requests": False,
                    "posts_per_page": 10
                }
            ):
                text = fb_post.get("text", "")
                post_url = fb_post.get("post_url", "")
                time = fb_post.get("time", "")
                likes = fb_post.get("likes", 0) or 0
                comments = fb_post.get("comments", 0) or 0
                shares = fb_post.get("shares", 0) or 0

                if not text:
                    continue

                engagement = likes + comments + shares

                post = {
                    "post_id": generate_post_id(text + page_name),
                    "platform": "Facebook",
                    "source": page_name,
                    "region": region,
                    "content": text[:500],
                    "timestamp": str(time),
                    "engagement": engagement,
                    "url": post_url
                }

                posts.append(post)

                count += 1
                if count >= 5:
                    break

            print(f"✅ {count} posts Facebook réels récupérés depuis {page_name}")

        except Exception as e:
            print(f"❌ Facebook bloqué pour {page_name}: {e}")

    return posts


# -----------------------------
# Fallback simulé
# -----------------------------
def fetch_local_mock_posts():
    local_posts = [
        {
            "platform": "Facebook",
            "source": "MOCK - Sfax News",
            "region": "Sfax",
            "content": "Accident grave sur la route de Sakiet Ezzit à Sfax 😨",
            "timestamp": datetime.now().isoformat(),
            "engagement": 320,
            "url": ""
        },
        {
            "platform": "Facebook",
            "source": "MOCK - Gabès Info",
            "region": "Gabès",
            "content": "Pollution industrielle signalée près de Gabès, colère des habitants 😡",
            "timestamp": datetime.now().isoformat(),
            "engagement": 450,
            "url": ""
        },
        {
            "platform": "Facebook",
            "source": "MOCK - Jendouba Actualités",
            "region": "Jendouba",
            "content": "Fortes pluies à Jendouba, plusieurs routes bloquées 😨",
            "timestamp": datetime.now().isoformat(),
            "engagement": 280,
            "url": ""
        },
        {
            "platform": "Facebook",
            "source": "MOCK - Tunis Alertes",
            "region": "Tunis",
            "content": "Embouteillage important au centre-ville de Tunis ce matin",
            "timestamp": datetime.now().isoformat(),
            "engagement": 190,
            "url": ""
        }
    ]

    for post in local_posts:
        post["post_id"] = generate_post_id(
            post["content"] + post["source"]
        )

    print(f"\n🧪 {len(local_posts)} posts Facebook simulés ajoutés comme fallback")

    return local_posts


# -----------------------------
# Sauvegarde SQLite
# -----------------------------
def save_posts(posts):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for post in posts:
        cursor.execute("""
        INSERT OR IGNORE INTO Posts (
            post_id,
            platform,
            source,
            region,
            content,
            timestamp,
            engagement,
            url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post["post_id"],
            post["platform"],
            post["source"],
            post["region"],
            post["content"],
            post["timestamp"],
            post["engagement"],
            post["url"]
        ))

    conn.commit()
    conn.close()

    print(f"\n💾 {len(posts)} posts sauvegardés dans SQLite")


# -----------------------------
# Affichage posts
# -----------------------------
def show_posts(limit=15):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT source, region, platform, content, timestamp, engagement
    FROM Posts
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    print("\n📊 Exemple des posts stockés :")

    for row in rows:
        print(
            f"- [{row[2]} | {row[0]}] "
            f"({row[1]}) {row[3]} | Engagement: {row[5]}"
        )


# -----------------------------
# Statistiques régionales
# -----------------------------
def show_region_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT region, COUNT(*)
    FROM Posts
    GROUP BY region
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n📍 Nombre de posts par région :")

    for region, count in rows:
        print(f"- {region}: {count}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    init_db()

    posts = []

    # RSS réels
    posts += fetch_rss()

    # Facebook réel (si possible)
    real_fb_posts = fetch_facebook_posts()
    posts += real_fb_posts

    # Fallback si Facebook réel insuffisant
    if len(real_fb_posts) < 4:
        posts += fetch_local_mock_posts()

    print(f"\n✅ Total posts trouvés : {len(posts)}")

    save_posts(posts)

    show_posts()

    show_region_stats()