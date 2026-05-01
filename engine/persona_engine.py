# persona_engine.py — Membre 4 : Persona Decision Engine
# ========================================================
# Transforme les données enrichies en décisions personnalisées
# selon le persona sélectionné.
#
# Intégration :
#   - Lit depuis database.py (pulseTN.db)
#   - Accepte aussi des EnrichedEvent Pydantic venant du backend (Membre 5)
#   - Expose get_dashboard() pour le frontend (Streamlit)
#   - Expose generate() pour le pipeline backend (interfaces.py)

import sys
import os

# Permet d'importer database.py même si on lance depuis la racine du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_recent_posts


# ══════════════════════════════════════════════════════════════════════════════
# ADAPTATEUR ÉMOTION
# Le Membre 3 produit EmotionScore {joy, anger, fear, sadness}
# Nos règles utilisent des chaînes françaises : "Panique", "Colère", etc.
# ══════════════════════════════════════════════════════════════════════════════

def emotion_score_to_label(emotion) -> str:
    """
    Convertit un EmotionScore (dict ou objet Pydantic) en label français.
    Compatible avec :
      - dict  : {"joy": 10, "anger": 70, "fear": 60, "sadness": 30}
      - objet : EmotionScore(joy=10, anger=70, fear=60, sadness=30)
      - str   : déjà un label → retourné tel quel
    """
    if isinstance(emotion, str):
        return emotion  # déjà un label (ex: seed_data)

    # Normalise en dict
    if hasattr(emotion, "__dict__"):
        e = vars(emotion)
    elif hasattr(emotion, "dict"):
        e = emotion.dict()
    elif isinstance(emotion, dict):
        e = emotion
    else:
        return "Neutre"

    scores = {
        "Panique":    e.get("fear",    0),
        "Colère":     e.get("anger",   0),
        "Tristesse":  e.get("sadness", 0),
        "Hype":       e.get("joy",     0),
        "Humour":     e.get("joy",     0) * 0.8,   # joy élevé + contexte léger
        "Solidarité": e.get("joy",     0) * 0.5,
    }

    dominant = max(scores, key=scores.get)
    return dominant if scores[dominant] > 0 else "Neutre"


def normalize_post(post) -> dict:
    """
    Normalise un post quelle que soit sa source :
      - dict brut SQLite (Membre 1 / seed_data)
      - EnrichedEvent Pydantic (pipeline Membre 5)
    Retourne toujours un dict uniforme.
    """
    if isinstance(post, dict):
        emotion_raw = post.get("emotion", "Neutre")
        return {
            "post_id":    post.get("post_id", "?"),
            "region":     post.get("region", "Tunis"),
            "category":   post.get("category", ""),
            "emotion":    emotion_score_to_label(emotion_raw),
            "viral_score": float(post.get("viral_score", 0)),
            "fake_score":  float(post.get("fake_score", 0)),
            "content":    post.get("content", ""),
            "timestamp":  post.get("timestamp", ""),
        }

    # Objet Pydantic (EnrichedEvent)
    return {
        "post_id":    getattr(post, "event_id", "?"),
        "region":     getattr(post, "region", "Tunis"),
        "category":   getattr(post, "category", ""),
        "emotion":    emotion_score_to_label(getattr(post, "emotion", "Neutre")),
        "viral_score": float(getattr(post, "viral_score", 0)),
        "fake_score":  float(getattr(post, "fake_score", 0)),
        "content":    " ".join(getattr(post, "keywords", [])),
        "timestamp":  "",
    }


# ══════════════════════════════════════════════════════════════════════════════
# RÈGLES PAR PERSONA
# ══════════════════════════════════════════════════════════════════════════════

def _score_journalist(post: dict) -> dict:
    recommendations = []
    priority = "NORMAL"

    if post["fake_score"] < 30 and post["viral_score"] > 60:
        recommendations.append("🚨 Vérifier et couvrir en priorité")
        priority = "HIGH"
    elif post["fake_score"] > 60:
        recommendations.append("⚠️ Source douteuse — vérification multiple requise")
        priority = "VERIFY"
    else:
        recommendations.append("📰 Signal faible — surveiller l'évolution")

    return {
        "priority":        priority,
        "recommendations": recommendations,
        "action":          "COVER" if priority == "HIGH" else "MONITOR"
    }


def _score_entreprise(post: dict) -> dict:
    recommendations = []
    decision = "GO"

    if post["emotion"] in ["Panique", "Colère"] and post["viral_score"] > 65:
        recommendations.append(f"⏸️ Pause campagne dans la région {post['region']}")
        decision = "PAUSE"
    elif post["emotion"] == "Tristesse" and post["viral_score"] > 50:
        recommendations.append("🔄 Adapter le ton — éviter contenu festif")
        decision = "ADAPT"
    else:
        recommendations.append("✅ Contexte favorable — campagne normale")

    brand_safety = (
        max(0, 100 - post["viral_score"])
        if post["emotion"] in ["Panique", "Colère"] else 85
    )

    return {
        "decision":          decision,
        "brand_safety_score": round(brand_safety, 1),
        "recommendations":   recommendations,
        "public_mood":       post["emotion"]
    }


def _score_influenceur(post: dict) -> dict:
    recommendations = []
    trend_safety = "WATCH"

    if post["viral_score"] > 75:
        if post["emotion"] in ["Hype", "Humour"]:
            recommendations.append("🔥 Trend exploitable — publie maintenant !")
            trend_safety = "SAFE"
        elif post["emotion"] in ["Panique", "Tristesse", "Colère"]:
            recommendations.append("🚫 Évite ce trend — contexte négatif")
            trend_safety = "DANGER"
        else:
            recommendations.append("👀 Trend à surveiller avant de publier")
    else:
        recommendations.append("💤 Pas de trend majeur en ce moment")

    best_time = "20h-22h" if post["emotion"] == "Hype" else "Attendre 24h"

    return {
        "trend_safety_score": trend_safety,
        "viral_score":        post["viral_score"],
        "best_posting_time":  best_time,
        "recommendations":    recommendations,
        "action":             "UTILISE" if trend_safety == "SAFE" else "EVITE"
    }


def _score_citoyen(post: dict) -> dict:
    recommendations = []
    alert_level = "INFO"

    if post["emotion"] == "Panique" and post["viral_score"] > 60:
        recommendations.append("🔴 Alerte sécurité — rester vigilant")
        alert_level = "DANGER"
    elif post["fake_score"] > 60:
        recommendations.append("⚠️ Information non vérifiée — fake warning")
        alert_level = "FAKE_WARNING"
    else:
        recommendations.append("ℹ️ Actualité locale — pas de danger immédiat")

    return {
        "alert_level":    alert_level,
        "recommendations": recommendations,
        "fake_warning":   post["fake_score"] > 60
    }


def _score_ong(post: dict) -> dict:
    recommendations = []
    intervention_needed = False

    if (post["category"] in ["Catastrophe", "Accident", "Protestation"]
            and post["viral_score"] > 55):
        recommendations.append(
            f"🆘 Intervention requise — zone prioritaire : {post['region']}"
        )
        intervention_needed = True
    else:
        recommendations.append("📊 Surveiller l'évolution dans la région")

    return {
        "intervention_needed": intervention_needed,
        "priority_zone":       post["region"],
        "sentiment_collectif": post["emotion"],
        "recommendations":     recommendations
    }


PERSONA_ENGINES = {
    "journaliste": _score_journalist,
    "entreprise":  _score_entreprise,
    "influenceur": _score_influenceur,
    "citoyen":     _score_citoyen,
    "ong":         _score_ong,
}


# ══════════════════════════════════════════════════════════════════════════════
# FONCTIONS PUBLIQUES
# ══════════════════════════════════════════════════════════════════════════════

def get_dashboard(persona_type: str, region: str = None) -> dict:
    """
    Fonction principale pour le frontend (Streamlit).
    Lit depuis pulseTN.db et retourne un dashboard JSON-friendly.

    Args:
        persona_type : "journaliste" | "entreprise" | "influenceur" | "citoyen" | "ong"
        region       : filtre optionnel (ex: "Sfax")

    Returns:
        dict avec clés : persona, region, total, insights (list)
    """
    persona_type = persona_type.lower().strip()

    if persona_type not in PERSONA_ENGINES:
        return {"error": f"Persona inconnu : '{persona_type}'. "
                         f"Valeurs acceptées : {list(PERSONA_ENGINES.keys())}"}

    raw_posts = get_recent_posts(limit=50, region=region)

    if not raw_posts:
        return {
            "persona":  persona_type,
            "region":   region or "national",
            "total":    0,
            "message":  "Aucune donnée disponible. Lance seed_data.py ou importe raw_data.db.",
            "insights": []
        }

    engine   = PERSONA_ENGINES[persona_type]
    insights = []

    for raw in raw_posts:
        post   = normalize_post(raw)
        result = engine(post)
        insights.append({**post, **result})

    # Tri par viral_score décroissant
    insights.sort(key=lambda x: x.get("viral_score", 0), reverse=True)

    return {
        "persona":  persona_type,
        "region":   region or "national",
        "total":    len(insights),
        "insights": insights[:10]   # top 10
    }


def generate(enriched_events: list, persona: str) -> dict:
    """
    Point d'intégration avec le backend (interfaces.py — Membre 5).
    Accepte une liste d'EnrichedEvent Pydantic ou de dicts.

    Args:
        enriched_events : liste d'EnrichedEvent (Pydantic) ou dicts
        persona         : nom du persona

    Returns:
        dict Dashboard compatible avec schemas.py
    """
    persona = persona.lower().strip()

    if persona not in PERSONA_ENGINES:
        return {"error": f"Persona inconnu : {persona}"}

    if not enriched_events:
        return {
            "persona":         persona,
            "top_events":      [],
            "alerts":          ["Aucune donnée disponible"],
            "recommendations": []
        }

    engine      = PERSONA_ENGINES[persona]
    top_events  = []
    alerts      = []
    all_recs    = []

    for raw in enriched_events:
        post   = normalize_post(raw)
        result = engine(post)

        # Collecte alertes urgentes
        if result.get("priority") == "HIGH" or result.get("alert_level") == "DANGER":
            alerts.append(
                f"🚨 [{post['region']}] {post['content'][:60]}..."
            )

        # Collecte recommandations
        for msg in result.get("recommendations", []):
            all_recs.append({"message": msg, "priority": 1 if "🚨" in msg else 3})

        top_events.append({**post, **result})

    top_events.sort(key=lambda x: x.get("viral_score", 0), reverse=True)

    return {
        "persona":         persona,
        "top_events":      top_events[:10],
        "alerts":          alerts[:5],
        "recommendations": all_recs[:10]
    }


# ── Test local ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("TEST persona_engine.py")
    print("=" * 60)

    for p in ["journaliste", "entreprise", "influenceur", "citoyen", "ong"]:
        print(f"\n{'─'*40}")
        print(f"  PERSONA : {p.upper()}")
        print(f"{'─'*40}")
        dash = get_dashboard(p)
        if dash.get("insights"):
            first = dash["insights"][0]
            print(f"  Région     : {first.get('region')}")
            print(f"  Émotion    : {first.get('emotion')}")
            print(f"  ViralScore : {first.get('viral_score')}")
            print(f"  Recomm.    : {first.get('recommendations', [])}")
        else:
            print(f"  {dash.get('message', 'Pas de données')}")

    print("\n✅ Tests terminés")