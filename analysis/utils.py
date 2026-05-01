"""
utils.py — PulseTN Persona | Shared Helpers
============================================
Auteur : Membre 3 — Emotion & Fake Detection
Rôle   : Fonctions utilitaires partagées par emotion_analyzer.py et fake_detector.py
"""

import re
import unicodedata
from datetime import datetime


def normalize_score(value: float, min_val: float = 0, max_val: float = 100) -> int:
    """
    Normalise une valeur brute vers une échelle 0-100.
    """
    if max_val == min_val:
        return 0

    value = max(min_val, min(value, max_val))
    normalized = (value - min_val) / (max_val - min_val) * 100
    return int(round(normalized))


def clean_text(text: str) -> str:
    """
    Nettoie le texte brut : supprime URLs, mentions, espaces inutiles.
    """
    if not text or not isinstance(text, str):
        return ""

    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"[^\S\n]+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    """
    Normalise le texte pour comparaison : minuscules, sans accents, ponctuation retirée.
    """
    if not text:
        return ""

    text = text.lower()

    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_keywords(text: str, keywords_list: list) -> list:
    """
    Extrait les mots-clés présents dans le texte.
    """
    if not text or not keywords_list:
        return []

    normalized = normalize_text(text)
    found = []

    for kw in keywords_list:
        kw_normalized = normalize_text(kw)
        pattern = r"\b" + re.escape(kw_normalized) + r"\b"

        if re.search(pattern, normalized):
            found.append(kw)

    return found


def standardize_output(post: dict) -> dict:
    """
    Construit la structure standardisée complète d'un post analysé.
    Compatible avec Membre 2, Membre 4 et Membre 5.
    """
    return {
        # ── Identité du post ──────────────────────────────────
        "post_id": post.get("post_id", _generate_id(post)),
        "region": post.get("region", "Unknown"),
        "platform": post.get("platform", "Unknown"),
        "source": post.get("source", "Unknown"),
        "content": post.get("content", ""),
        "category": post.get("category", "Unknown"),
        "timestamp": post.get("timestamp", datetime.utcnow().isoformat()),

        # ── Scores Émotion ────────────────────────────────────
        "emotion": post.get("emotion", "neutral"),
        "emotion_score": post.get("emotion_score", 0),
        "secondary_emotion": post.get("secondary_emotion") or "neutral",
        "confidence_index": post.get("confidence_index", post.get("emotion_score", 0)),
        "emojis": post.get("emojis", []),

        # ── Scores Fake News ──────────────────────────────────
        "fake_score": post.get("fake_score", 0),
        "risk_level": post.get("risk_level", "Low"),
        "flags": post.get("flags", []),

        # ── Score Viral ───────────────────────────────────────
        "viral_score": post.get("viral_score", 0),

        # ── Scores détaillés ──────────────────────────────────
        "sensationalism_score": post.get("sensationalism_score", 0),
        "credibility_score": post.get("credibility_score", 50),
    }


def _generate_id(post: dict) -> str:
    """
    Génère un ID simple basé sur timestamp + source.
    """
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    src = post.get("source", "unknown")[:8].replace(" ", "_")
    return f"{src}_{ts}"


def score_to_risk_level(score: int) -> str:
    """
    Convertit un score 0-100 en niveau de risque.
    """
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


if __name__ == "__main__":
    print("=== Test utils.py ===\n")

    assert normalize_score(75) == 75
    assert normalize_score(150) == 100
    assert normalize_score(-10) == 0
    print("✓ normalize_score OK")

    raw = "  Check https://example.com @user123 #Tunisie Incroyable!!!  "
    cleaned = clean_text(raw)
    print(f"✓ clean_text: '{cleaned}'")

    normed = normalize_text("Catastrophe à Gabès!! Réseau 🔥")
    print(f"✓ normalize_text: '{normed}'")

    found = extract_keywords(
        "Accident grave à Sfax ce matin",
        ["accident", "incendie", "sfax"]
    )
    print(f"✓ extract_keywords: {found}")

    output = standardize_output({
        "content": "Test post",
        "region": "Tunis",
        "emotion": "anger",
        "emotion_score": 85,
        "fake_score": 30
    })
    print(f"✓ standardize_output keys: {list(output.keys())}")

    assert score_to_risk_level(80) == "High"
    assert score_to_risk_level(55) == "Medium"
    assert score_to_risk_level(20) == "Low"
    print("✓ score_to_risk_level OK")

    print("\n✅ Tous les tests utils.py passent.")