import sqlite3


DB_PATH = "../data/raw_data.db"


def create_tables():
    # Placeholder : la DB existe déjà
    return True


def detect_category(text):
    text = text.lower()

    if any(word in text for word in ["accident", "حادث", "blessés", "grave"]):
        return "Accident"
    if any(word in text for word in ["orage", "pluie", "météo", "chaleur", "inm"]):
        return "Météo"
    if any(word in text for word in ["challenge", "tiktok", "viral", "hashtag"]):
        return "Trend viral"
    if any(word in text for word in ["festival", "culture", "fête"]):
        return "Culture"

    return "News"


def viral_score(engagement, category):
    score = engagement

    if category in ["Accident", "Météo"]:
        score += 60
    elif category == "Trend viral":
        score += 40
    elif category == "Culture":
        score += 10

    return max(0, min(score, 100))


def load_raw_posts_into_engine(limit=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content, source, region, platform, engagement
        FROM posts
    """)

    posts = []

    for content, source, region, platform, engagement in cursor.fetchall():
        category = detect_category(content)
        score = viral_score(engagement, category)

        posts.append({
            "content": content,
            "source": source,
            "region": region,
            "platform": platform,
            "engagement": engagement,
            "category": category,
            "viral_score": score
        })

    conn.close()

    return posts