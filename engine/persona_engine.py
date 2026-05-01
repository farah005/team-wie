# persona_engine.py
from database import get_recent_posts

# -------------------------------
# Règles pour chaque persona
# -------------------------------

def _score_journalist(post):
    recommendations = []
    priority = "NORMAL"
    if post["fake_score"] < 30 and post["viral_score"] > 60:
        recommendations.append("🚨 Vérifier et couvrir en priorité")
        priority = "HIGH"
    elif post["fake_score"] > 60:
        recommendations.append("⚠️ Source douteuse – vérification multiple requise")
        priority = "VERIFY"
    else:
        recommendations.append("📰 Signal faible – surveiller l'évolution")
    return {
        "priority": priority,
        "recommendations": recommendations,
        "action": "COVER" if priority == "HIGH" else "MONITOR"
    }

def _score_entreprise(post):
    recommendations = []
    decision = "GO"
    if post["emotion"] in ["Panique", "Colère"] and post["viral_score"] > 65:
        recommendations.append(f"⏸️ Pause campagne dans la région {post['region']}")
        decision = "PAUSE"
    elif post["emotion"] in ["Tristesse"] and post["viral_score"] > 50:
        recommendations.append("🔄 Adapter le ton – éviter contenu festif")
        decision = "ADAPT"
    else:
        recommendations.append("✅ Contexte favorable – campagne normale")
        decision = "GO"
    brand_safety_score = max(0, 100 - post["viral_score"]) if post["emotion"] in ["Panique", "Colère"] else 85
    return {
        "decision": decision,
        "brand_safety_score": brand_safety_score,
        "recommendations": recommendations,
        "public_mood": post["emotion"]
    }

def _score_influenceur(post):
    recommendations = []
    trend_safety = "SAFE"
    if post["viral_score"] > 75:
        if post["emotion"] in ["Hype", "Humour"]:
            recommendations.append("🔥 Trend exploitable – publie maintenant !")
            trend_safety = "SAFE"
        elif post["emotion"] in ["Panique", "Tristesse", "Colère"]:
            recommendations.append("🚫 Évite ce trend – contexte négatif")
            trend_safety = "DANGER"
        else:
            recommendations.append("👀 Trend à surveiller avant de publier")
            trend_safety = "WATCH"
    else:
        recommendations.append("💤 Pas de trend majeur en ce moment")
    best_time = "20h-22h" if post["emotion"] == "Hype" else "Attendre 24h"
    return {
        "trend_safety_score": trend_safety,
        "viral_score": post["viral_score"],
        "best_posting_time": best_time,
        "recommendations": recommendations,
        "action": "UTILISE" if trend_safety == "SAFE" else "EVITE"
    }

def _score_citoyen(post):
    recommendations = []
    alert_level = "INFO"
    if post["emotion"] == "Panique" and post["viral_score"] > 60:
        recommendations.append("🔴 Alerte sécurité – rester vigilant")
        alert_level = "DANGER"
    elif post["fake_score"] > 60:
        recommendations.append("⚠️ Information non vérifiée – fake warning")
        alert_level = "FAKE_WARNING"
    else:
        recommendations.append("ℹ️ Actualité locale – pas de danger immédiat")
        alert_level = "INFO"
    return {
        "alert_level": alert_level,
        "recommendations": recommendations,
        "fake_warning": post["fake_score"] > 60
    }

def _score_ong(post):
    recommendations = []
    intervention_needed = False
    if post["category"] in ["Catastrophe", "Accident", "Protestation"] and post["viral_score"] > 55:
        recommendations.append(f"🆘 Intervention requise – zone prioritaire : {post['region']}")
        intervention_needed = True
    else:
        recommendations.append("📊 Surveiller l'évolution dans la région")
    return {
        "intervention_needed": intervention_needed,
        "priority_zone": post["region"],
        "sentiment_collectif": post["emotion"],
        "recommendations": recommendations
    }

# -------------------------------
# Moteur principal
# -------------------------------

PERSONA_ENGINES = {
    "journaliste": _score_journalist,
    "entreprise": _score_entreprise,
    "influenceur": _score_influenceur,
    "citoyen": _score_citoyen,
    "ong": _score_ong,
}

def get_dashboard(persona_type: str, region: str = None) -> dict:
    """
    Fonction principale appelée par le backend ou le frontend.
    Retourne un tableau de bord personnalisé.
    """
    persona_type = persona_type.lower()
    if persona_type not in PERSONA_ENGINES:
        return {"error": f"Persona inconnu : {persona_type}"}

    posts = get_recent_posts(limit=50, region=region)
    if not posts:
        return {
            "persona": persona_type,
            "message": "Aucune donnée disponible pour le moment.",
            "insights": []
        }

    engine = PERSONA_ENGINES[persona_type]
    insights = []
    for post in posts:
        result = engine(post)
        insights.append({
            "post_id": post["post_id"],
            "region": post["region"],
            "category": post["category"],
            "emotion": post["emotion"],
            "viral_score": post["viral_score"],
            "fake_score": post["fake_score"],
            "timestamp": post["timestamp"],
            **result
        })

    # Trier par viral_score décroissant
    insights.sort(key=lambda x: x.get("viral_score", 0), reverse=True)

    return {
        "persona": persona_type,
        "region": region or "national",
        "total": len(insights),
        "insights": insights[:10]  # top 10
    }

# Test rapide
if __name__ == "__main__":
    import json
    for p in ["journaliste", "entreprise", "influenceur", "citoyen", "ong"]:
        print(f"\n--- {p.upper()} ---")
        dash = get_dashboard(p)
        print(json.dumps(dash, ensure_ascii=False, indent=2))