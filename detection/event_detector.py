from .viral_score import calculate_viral_score


REGIONS = [
    "Tunis", "Ariana", "Ben Arous", "Manouba",
    "Sfax", "Sousse", "Monastir", "Mahdia",
    "Gabès", "Medenine", "Médenine", "Tataouine",
    "Nabeul", "Bizerte", "Beja", "Béja", "Jendouba",
    "Kef", "Siliana", "Kairouan", "Kasserine",
    "Sidi Bouzid", "Gafsa", "Tozeur", "Kebili", "Kébili",
    "Zaghouan"
]


CATEGORIES_KEYWORDS = {
    "Accident": [
        "accident", "collision", "mort", "blessé", "blessés",
        "route", "carambolage", "crash", "7adeth", "hadeth"
    ],

    "Catastrophe": [
        "inondation", "feu", "incendie", "séisme", "seisme",
        "tempête", "tempete", "catastrophe", "karitha", "flood"
    ],

    "Protestation": [
        "manifestation", "grève", "greve", "protestation",
        "colère", "colere", "sit-in", "ihtijaj", "e7tijaj"
    ],

    "Politique": [
        "ministre", "président", "president", "gouvernement",
        "élection", "election", "parti", "parlement"
    ],

    "Culture": [
        "festival", "concert", "exposition", "théâtre",
        "theatre", "cinéma", "cinema", "spectacle"
    ],

    "Trend viral": [
        "trend", "viral", "tiktok", "challenge", "hashtag",
        "buzz", "reel", "instagram", "youtube shorts"
    ]
}


def detect_region(text):
    text_lower = str(text).lower()

    for region in REGIONS:
        if region.lower() in text_lower:
            return region

    return "Tunisie"


def categorize_event(text):
    text_lower = str(text).lower()

    for category, keywords in CATEGORIES_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return category

    return "Autre"


def detect_signal_strength(post):
    engagement = post.get("engagement", 0)
    growth = post.get("growth", 0)

    try:
        engagement = float(engagement)
        growth = float(growth)
    except (ValueError, TypeError):
        engagement = 0
        growth = 0

    if growth >= 60 and engagement <= 40:
        return "Signal faible émergent"
    elif engagement >= 70 or growth >= 80:
        return "Événement fort"
    else:
        return "Normal"


def calculate_priority_score(category, viral_score):
    if category in ["Accident", "Catastrophe"]:
        return min(viral_score + 20, 100)

    if category == "Protestation":
        return min(viral_score + 10, 100)

    return viral_score


def enrich_post(post, max_values):
    content = str(post.get("content", "")).strip()

    post["region"] = detect_region(content)
    post["category"] = categorize_event(content)
    post["viral_score"] = calculate_viral_score(post, max_values)
    post["signal"] = detect_signal_strength(post)
    post["priority_score"] = calculate_priority_score(
        post["category"],
        post["viral_score"]
    )

    return post


def analyze_posts(posts):
    if not posts:
        return []

    max_values = {
        "volume": max([p.get("volume", 0) for p in posts], default=1),
        "engagement": max([p.get("engagement", 0) for p in posts], default=1),
        "growth": max([p.get("growth", 0) for p in posts], default=1),
        "platform_count": max([p.get("platform_count", 1) for p in posts], default=1),
    }

    enriched_posts = []

    for post in posts:
        enriched_posts.append(enrich_post(post, max_values))

    return enriched_posts


def get_top_events(posts, limit=5):
    return sorted(
        posts,
        key=lambda x: x.get("priority_score", 0),
        reverse=True
    )[:limit]