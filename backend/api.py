
from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sqlite3, statistics
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List

try:
    from backend.services.pipeline import run_full_pipeline
except Exception:
    run_full_pipeline = None

app = FastAPI(title="Tnassnissa Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
PULSE_DB = BASE_DIR / "engine" / "pulseTN.db"
RAW_DB = BASE_DIR / "data" / "raw_data.db"

BUSINESS_INTERESTS = {
    "mode": {
        "label": "Mode",
        "keywords": [
            "mode", "fashion", "textile", "vetement", "vÃªtement", "look",
            "collection", "style", "beauty", "beaute", "boutique", "lifestyle",
        ],
    },
    "grand_surface": {
        "label": "Grand surface",
        "keywords": [
            "grand surface", "grande surface", "magasin", "supermarche",
            "supermarchÃ©", "retail", "commerce", "promotion", "promo",
            "prix", "achat", "client", "consommation",
        ],
    },
    "sport": {
        "label": "Sport",
        "keywords": [
            "sport", "sports", "match", "football", "foot", "stade",
            "equipe", "Ã©quipe", "club", "joueur", "tournoi", "fitness",
        ],
    },
}

PERSONA_LABELS = {
    "journaliste": ("Mode: Journaliste", "Profil: Journaliste"),
    "entreprise": ("Mode: Entreprise", "Profil: Entreprise"),
    "influenceur": ("Mode: Influenceur", "Profil: Influenceur"),
    "citoyen": ("Mode: Citoyen", "Profil: Citoyen"),
    "ong": ("Mode: ONG", "Profil: ONG"),
}
EMOJI = {"Colère":"😡", "Panique":"😰", "Tristesse":"😢", "Hype":"🔥", "Joie":"😂", "Humour":"😂", "Neutre":"🙂"}

def _rows(db: Path, sql: str, params=()):
    if not db.exists(): return []
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    try:
        cur = con.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]
    finally:
        con.close()

def load_posts() -> List[Dict[str, Any]]:
    rows = _rows(PULSE_DB, "SELECT post_id, region, platform, source, content, category, emotion, viral_score, fake_score, timestamp FROM posts ORDER BY timestamp DESC")
    if rows: return rows
    raw = _rows(RAW_DB, "SELECT post_id, platform, source, region, content, timestamp, engagement, url FROM Posts ORDER BY timestamp DESC")
    for r in raw:
        r["category"] = _guess_category(r.get("content", ""))
        r["emotion"] = _guess_emotion(r.get("content", ""))
        r["viral_score"] = min(100, int(r.get("engagement") or 0))
        r["fake_score"] = 20
    return raw

def _guess_category(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["accident", "incendie", "grave"]): return "Accident"
    if any(w in t for w in ["sport", "match", "football", "stade", "club"]): return "Sport"
    if any(w in t for w in ["mode", "fashion", "textile", "collection", "look"]): return "Mode"
    if any(w in t for w in ["magasin", "grand surface", "grande surface", "supermarche", "retail", "promotion"]): return "Grand surface"
    if any(w in t for w in ["challenge", "viral", "tiktok", "son"]): return "Trend viral"
    if any(w in t for w in ["festival", "musique", "culture"]): return "Culture"
    if any(w in t for w in ["élection", "politique"]): return "Politique"
    return "Actualité locale"

def _guess_emotion(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["accident", "incendie", "grave", "panique"]): return "Panique"
    if any(w in t for w in ["annulé", "triste"]): return "Tristesse"
    if any(w in t for w in ["viral", "challenge", "trend"]): return "Hype"
    return "Neutre"

def status_for(viral, fake, safe):
    if fake >= 38 or viral >= 82 or safe <= 40: return "Danger"
    if viral >= 60: return "Buzz"
    return "Stable"

def color_for(status):
    return {"Danger":"var(--red)", "Buzz":"var(--orange)", "Stable":"var(--green)"}.get(status, "var(--cyan)")

def normalize_business_interest(value: str | None) -> str | None:
    value = (value or "").strip().lower().replace("-", "_")
    return value if value in BUSINESS_INTERESTS else None

def post_matches_business_interest(post: Dict[str, Any], business_interest: str | None) -> bool:
    interest = normalize_business_interest(business_interest)
    if not interest:
        return True
    text = " ".join(
        str(post.get(key, "") or "").lower()
        for key in ["content", "category", "source", "platform"]
    )
    return any(keyword.lower() in text for keyword in BUSINESS_INTERESTS[interest]["keywords"])

def filter_posts_by_business_interest(posts: List[Dict[str, Any]], persona: str, business_interest: str | None) -> List[Dict[str, Any]]:
    interest = normalize_business_interest(business_interest)
    if persona != "entreprise" or not interest:
        return posts
    return [post for post in posts if post_matches_business_interest(post, interest)]

def business_interest_backup_posts(interest: str | None) -> List[Dict[str, Any]]:
    interest = normalize_business_interest(interest)
    if not interest:
        return []
    examples = {
        "mode": [
            ("Tunis", "Mode", "Mode: nouvelle collection fashion locale, forte interaction sur les looks printemps."),
            ("Sousse", "Mode", "Textile et boutiques: hausse des recherches autour des promotions vetements."),
        ],
        "grand_surface": [
            ("Sfax", "Grand surface", "Grand surface: affluence magasin et discussions clients autour des prix."),
            ("Tunis", "Grand surface", "Retail: promotions supermarche en tendance, opportunite campagne prudente."),
        ],
        "sport": [
            ("Tunis", "Sport", "Sport: match de football tres commente, pic de conversations autour des clubs."),
            ("Sousse", "Sport", "Sport regional: tournoi et equipements fitness en hausse sur les reseaux."),
        ],
    }
    now = datetime.utcnow().isoformat()
    return [
        {
            "post_id": f"business_{interest}_{idx}",
            "region": region,
            "platform": "Simulation",
            "source": f"Backup {BUSINESS_INTERESTS[interest]['label']}",
            "content": content,
            "category": category,
            "emotion": "Neutre",
            "viral_score": 55 + idx * 10,
            "fake_score": 15,
            "timestamp": now,
        }
        for idx, (region, category, content) in enumerate(examples[interest], start=1)
    ]

def build_regions(posts):
    grouped = defaultdict(list)
    for p in posts:
        region = (p.get("region") or "National").strip() or "National"
        grouped[region].append(p)
    regions = []
    for region, items in grouped.items():
        virals = [float(i.get("viral_score") or 0) for i in items]
        fakes = [float(i.get("fake_score") or 0) for i in items]
        viral = round(statistics.mean(virals), 1) if virals else 0
        fake = round(statistics.mean(fakes), 1) if fakes else 0
        safe = max(0, min(100, round(100 - fake - (viral/6), 1)))
        emotion = Counter([i.get("emotion") or "Neutre" for i in items]).most_common(1)[0][0]
        category = Counter([i.get("category") or "Actualité" for i in items]).most_common(1)[0][0]
        status = status_for(viral, fake, safe)
        top = max(items, key=lambda x: float(x.get("viral_score") or 0))
        summary = f"{category} détecté à {region}. {len(items)} signal(s), viral score moyen {viral}, fake risk {fake}. Dernier signal: {top.get('content','')[:120]}"
        regions.append({
            "key": region.lower().replace("è","e").replace("é","e").replace(" ","-"),
            "name": region, "status": status, "color": color_for(status), "viral": viral,
            "safe": safe, "fake": fake, "mood": EMOJI.get(emotion, "🙂"),
            "emotion": emotion, "category": category, "summary": summary,
            "info": {
                "event": f"🚨 Événement: {top.get('content','Signal régional')} — source {top.get('source','backend')}.",
                "trend": f"🔥 Trend: catégorie dominante {category}, plateforme principale {Counter([i.get('platform') or 'N/A' for i in items]).most_common(1)[0][0]}.",
                "advice": advice_for(status, category, emotion),
                "source": "🔎 Source: données backend SQLite pulseTN/raw_data, agrégées en temps réel par région."
            },
            "posts": items[:8]
        })
    return sorted(regions, key=lambda r: r["viral"], reverse=True)

def advice_for(status, category, emotion):
    if status == "Danger": return f"🤖 Conseil IA: contexte sensible ({emotion}). Évitez les campagnes joyeuses; privilégiez un ton informatif et empathique."
    if status == "Buzz": return f"🤖 Conseil IA: opportunité exploitable autour de {category}; publier avec ton léger mais surveiller les réactions."
    return "🤖 Conseil IA: communication normale possible, risque faible; continuer le monitoring."

def build_dashboard(persona="journaliste", business_interest: str | None = None):
    selected_interest = normalize_business_interest(business_interest)
    posts = filter_posts_by_business_interest(load_posts(), persona, selected_interest)
    if persona == "entreprise" and selected_interest and not posts:
        posts = business_interest_backup_posts(selected_interest)
    regions = build_regions(posts)
    total = len(posts)
    avg_viral = round(statistics.mean([float(p.get("viral_score") or 0) for p in posts]), 1) if posts else 0
    avg_fake = round(statistics.mean([float(p.get("fake_score") or 0) for p in posts]), 1) if posts else 0
    active_regions = len({p.get("region") for p in posts if p.get("region")})
    platforms = len({p.get("platform") for p in posts if p.get("platform")})
    emotions = Counter([p.get("emotion") or "Neutre" for p in posts])
    categories = Counter([p.get("category") or "Actualité" for p in posts])
    top_regions = regions[:2] or []
    labels = PERSONA_LABELS.get(persona, PERSONA_LABELS["journaliste"])
    interest_label = BUSINESS_INTERESTS[selected_interest]["label"] if persona == "entreprise" and selected_interest else None
    danger = [r for r in regions if r["status"] == "Danger"]
    buzz = [r for r in regions if r["status"] == "Buzz"]
    stable = [r for r in regions if r["status"] == "Stable"]
    def card(icon,title,text): return {"icon":icon,"title":title,"text":text}
    summary = [
        card("📡", "Signaux détectés", f"{total} posts analysés depuis le backend, {active_regions} régions actives, {platforms} plateformes."),
        card("🔥", "Top viral", f"{top_regions[0]['name'] if top_regions else 'N/A'} domine avec un score {top_regions[0]['viral'] if top_regions else 0}."),
        card("⚠️", "Risque", f"{len(danger)} régions en danger, fake risk moyen {avg_fake}%."),
    ]
    persona_intro = {
        "journaliste":"Priorité aux alertes vérifiables, sources et signaux forts.",
        "entreprise":"Priorité au SafeAd Score, bad buzz et risque réputationnel.",
        "influenceur":"Priorité aux trends, timing de publication et hashtags exploitables.",
        "citoyen":"Priorité au résumé local et aux alertes sécurité.",
        "ong":"Priorité aux zones sensibles et besoins d’intervention."
    }.get(persona, "Vue générale")
    if interest_label:
        persona_intro = f"Priorite aux signaux {interest_label}, SafeAd Score, bad buzz et risque reputationnel."
    recos = [
        {"icon":"🤖", "text":f"<strong>{labels[1].replace('Profil: ', '').upper()}:</strong> {persona_intro}"},
        {"icon":"🚨", "text":f"<strong>ALERTE:</strong> {danger[0]['name']+' est en état Danger.' if danger else 'Aucune région en danger critique actuellement.'}"},
        {"icon":"📈", "text":f"<strong>OPPORTUNITÉ:</strong> {buzz[0]['name']+' montre un buzz exploitable.' if buzz else 'Peu de buzz exploitable pour le moment.'}"},
    ]
    alerts = []
    for r in regions[:5]:
        badge = "danger" if r["status"]=="Danger" else "warning" if r["status"]=="Buzz" else "info"
        icon = "🚨" if badge=="danger" else "🔥" if badge=="warning" else "✅"
        alerts.append({"icon":icon,"title":f"{r['name']} — {r['status']}","desc":r["summary"],"meta":f"{r['category']} · viral {r['viral']} · fake {r['fake']}","badge":badge})
    mood_total = sum(emotions.values()) or 1
    mood = [{"name":k,"emoji":EMOJI.get(k,"🙂"),"pct":round(v*100/mood_total)} for k,v in emotions.most_common(4)]
    while len(mood)<4: mood.append({"name":"Neutre","emoji":"🙂","pct":0})
    ticker = [f"{r['status']} à {r['name']} · viral {r['viral']}" for r in regions[:8]]
    left = regions[0] if regions else None
    right = regions[1] if len(regions)>1 else left
    return {
        "persona": persona, "businessInterest": selected_interest, "businessInterestLabel": interest_label,
        "label": f"{labels[0]} - {interest_label}" if interest_label else labels[0], "recoLabel": labels[1],
        "kpis": {"pulse": active_regions, "viral": avg_viral, "safe": max(0, round(100-avg_fake-(avg_viral/8),1)), "buzzLife":"14h", "risk":"HIGH" if danger else "MEDIUM" if buzz else "LOW"},
        "regions": regions, "summary": summary, "recos": recos, "alerts": alerts, "mood": mood,
        "scores": {"tnassnissa": avg_viral, "safead": max(0, round(100-avg_fake-(avg_viral/8),1)), "heat": round(avg_viral + len(danger)*5,1)},
        "trendBattle": {"left": left, "right": right}, "ticker": ticker,
        "detail": {"title":"Dashboard connecté", "body": f"Données chargées depuis {PULSE_DB.name if PULSE_DB.exists() else RAW_DB.name}."}
    }

@app.get("/")
def home(): return {"status":"ok", "message":"Tnassnissa backend ready"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

@app.get("/dashboard/{persona}")
def old_dashboard(persona: str, business_interest: str | None = Query(None)):
    if run_full_pipeline and not normalize_business_interest(business_interest):
        try: return run_full_pipeline(persona)
        except Exception: pass
    return build_dashboard(persona, business_interest)

@app.get("/api/dashboard/{persona}")
def dashboard(persona: str, business_interest: str | None = Query(None)): return build_dashboard(persona, business_interest)

@app.get("/api/regions")
def regions(): return {"regions": build_regions(load_posts())}

@app.get("/api/region/{region}")
def region(region: str):
    key = region.lower().replace("è","e").replace("é","e").replace(" ","-")
    for r in build_regions(load_posts()):
        if r["key"] == key or r["name"].lower() == region.lower(): return r
    return {"error":"region not found", "region": region}

@app.get("/api/detail/{kind}/{key}")
def detail(kind: str, key: str = "all", persona: str = Query("journaliste"), business_interest: str | None = Query(None)):
    data = build_dashboard(persona, business_interest)
    return {"kind": kind, "key": key, "title": f"Détail {kind}", "body": data.get("detail",{}).get("body",""), "dashboard": data}
