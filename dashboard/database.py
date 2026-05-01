# database.py — PulseTN Data Layer
import sqlite3, os, random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "raw_data.db")

MOCK_POSTS = [
    {"post_id":1,"platform":"Facebook","source":"Groupe Sfax Actu","region":"Sfax","content":"Accident grave sur l'autoroute A1 — circulation bloquée","timestamp":"2026-05-01 08:30:00","engagement":1240,"url":"","category":"Accident","emotion":"Panique","viral_score":88,"fake_score":10},
    {"post_id":2,"platform":"TikTok","source":"TikTok TN Trends","region":"Tunis","content":"Nouveau son viral #PulseTN challenge — tout le monde danse","timestamp":"2026-05-01 10:15:00","engagement":45000,"url":"","category":"Trend viral","emotion":"Hype","viral_score":96,"fake_score":3},
    {"post_id":3,"platform":"Facebook","source":"Gabès Infos","region":"Gabès","content":"Incendie dans la zone industrielle — évacuation en cours","timestamp":"2026-05-01 07:45:00","engagement":8900,"url":"","category":"Catastrophe","emotion":"Panique","viral_score":91,"fake_score":8},
    {"post_id":4,"platform":"Google Trends","source":"Google TN","region":"Tunis","content":"Hausse massive des recherches sur les élections municipales","timestamp":"2026-05-01 09:00:00","engagement":3200,"url":"","category":"Politique","emotion":"Colère","viral_score":72,"fake_score":35},
    {"post_id":5,"platform":"Instagram","source":"Sousse Events","region":"Sousse","content":"Festival Médina Jazz annulé — remboursements en cours","timestamp":"2026-05-01 11:30:00","engagement":2100,"url":"","category":"Culture","emotion":"Tristesse","viral_score":60,"fake_score":12},
    {"post_id":6,"platform":"RSS","source":"Realites.tn","region":"Tunis","content":"Nouvelle loi sur les startups : avantages fiscaux étendus","timestamp":"2026-05-01 06:00:00","engagement":980,"url":"","category":"Économie","emotion":"Neutre","viral_score":45,"fake_score":5},
    {"post_id":7,"platform":"TikTok","source":"TikTok TN","region":"Nabeul","content":"Tendance été : les plages de Nabeul envahies par les touristes","timestamp":"2026-05-01 12:00:00","engagement":28000,"url":"","category":"Tourisme","emotion":"Hype","viral_score":85,"fake_score":4},
    {"post_id":8,"platform":"Facebook","source":"Bizerte Today","region":"Bizerte","content":"Coupures d'eau programmées dans plusieurs quartiers","timestamp":"2026-05-01 08:00:00","engagement":4500,"url":"","category":"Infrastructure","emotion":"Colère","viral_score":67,"fake_score":15},
    {"post_id":9,"platform":"Instagram","source":"Fashion TN","region":"Tunis","content":"Les robes tunisiennes s'invitent sur les podiums de Paris","timestamp":"2026-05-01 14:00:00","engagement":15000,"url":"","category":"Mode","emotion":"Hype","viral_score":78,"fake_score":6},
    {"post_id":10,"platform":"RSS","source":"AfricanManager","region":"Sfax","content":"Investissements étrangers en hausse de 30% dans la région","timestamp":"2026-05-01 09:30:00","engagement":1200,"url":"","category":"Économie","emotion":"Neutre","viral_score":50,"fake_score":8},
    {"post_id":11,"platform":"Facebook","source":"Kairouan News","region":"Kairouan","content":"Protestation devant la mairie suite à coupures d'électricité","timestamp":"2026-05-01 10:45:00","engagement":6700,"url":"","category":"Protestation","emotion":"Colère","viral_score":80,"fake_score":18},
    {"post_id":12,"platform":"TikTok","source":"Sport TN Viral","region":"Tunis","content":"L'Espérance Sportive remporte le championnat — explosion de joie","timestamp":"2026-05-01 22:00:00","engagement":92000,"url":"","category":"Sport","emotion":"Hype","viral_score":98,"fake_score":2},
    {"post_id":13,"platform":"RSS","source":"Mosaique FM","region":"Médenine","content":"Naufrage en Méditerranée — 40 personnes secourues","timestamp":"2026-05-01 03:00:00","engagement":18000,"url":"","category":"Catastrophe","emotion":"Panique","viral_score":89,"fake_score":20},
    {"post_id":14,"platform":"Instagram","source":"Food TN","region":"Sousse","content":"Restaurant Le Pêcheur élu meilleur resto de Tunisie 2026","timestamp":"2026-05-01 13:00:00","engagement":9800,"url":"","category":"Gastronomie","emotion":"Hype","viral_score":71,"fake_score":5},
    {"post_id":15,"platform":"Facebook","source":"Gafsa Actualités","region":"Gafsa","content":"Grève des mineurs — routes bloquées depuis ce matin","timestamp":"2026-05-01 07:00:00","engagement":11200,"url":"","category":"Protestation","emotion":"Colère","viral_score":84,"fake_score":22},
]

def get_connection():
    if not os.path.exists(DB_PATH):
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None

def get_posts(limit=200, region=None, platform=None):
    conn = get_connection()
    if conn is None:
        posts = MOCK_POSTS.copy()
        if region and region != "Toutes":
            posts = [p for p in posts if p["region"] == region]
        if platform and platform != "Toutes":
            posts = [p for p in posts if p["platform"] == platform]
        return posts[:limit]
    try:
        q = "SELECT * FROM posts"
        conds, params = [], []
        if region and region != "Toutes":
            conds.append("region=?"); params.append(region)
        if platform and platform != "Toutes":
            conds.append("platform=?"); params.append(platform)
        if conds:
            q += " WHERE " + " AND ".join(conds)
        q += f" ORDER BY timestamp DESC LIMIT {limit}"
        rows = conn.execute(q, params).fetchall()
        conn.close()
        result = [dict(r) for r in rows]
        # Enrichir avec champs manquants
        for p in result:
            if "viral_score" not in p:  p["viral_score"] = random.randint(30,90)
            if "fake_score"  not in p:  p["fake_score"]  = random.randint(5,40)
            if "category"    not in p:  p["category"]    = "Général"
            if "emotion"     not in p:  p["emotion"]     = "Neutre"
        return result
    except:
        return MOCK_POSTS[:limit]

def get_stats(posts):
    total    = len(posts)
    crises   = sum(1 for p in posts if p.get("emotion") in ["Panique","Colère"] and p.get("viral_score",0)>65)
    oppos    = sum(1 for p in posts if p.get("emotion") in ["Hype"] and p.get("viral_score",0)>70)
    regions  = {}
    for p in posts:
        r = p.get("region","?")
        regions[r] = regions.get(r,0) + 1
    sources  = {}
    for p in posts:
        s = p.get("source","?")
        sources[s] = sources.get(s,0) + 1
    top_region = max(regions, key=regions.get) if regions else "—"
    top_source = max(sources, key=sources.get) if sources else "—"
    return {"total":total,"crises":crises,"oppos":oppos,"top_region":top_region,"top_source":top_source,"regions":regions,"sources":sources}
