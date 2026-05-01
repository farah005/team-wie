"""
emotion_analyzer.py — PulseTN Persona | Module 4 : Emoji & Emotion Intelligence
=================================================================================
Auteur : Membre 3 — Emotion & Fake Detection
Rôle   : Analyse émotionnelle de posts sociaux tunisiens (FR + AR + Darija + emojis)

Inputs  : post dict { content, region, source, ... }
Outputs : post enrichi avec emotion, emotion_score, emojis (0-100)

Intégration :
  - → Membre 4 (Persona Engine) : utilise emotion + emotion_score pour recommandations
  - → Membre 2 (Viral Score)    : emotion "hype"/"anger" booste le viral_score
  - → Membre 5 (Backend)        : via process_post() dans fake_detector.py
"""

import re
import emoji as emoji_lib

from analysis.utils import (
    clean_text,
    normalize_text,
    extract_keywords,
    normalize_score,
    standardize_output,
)


# ═══════════════════════════════════════════════════════════════════════════════
# LEXIQUES ÉMOTIONNELS
# Extensibles : ajouter mots sans toucher la logique
# ═══════════════════════════════════════════════════════════════════════════════

# Mapping emoji → émotion cible
EMOJI_EMOTION_MAP: dict[str, str] = {
    # Tristesse
    "😢": "sadness", "😭": "sadness", "💔": "sadness", "😿": "sadness",
    "🥺": "sadness", "😞": "sadness", "😔": "sadness",
    # Colère
    "😡": "anger",   "🤬": "anger",   "😤": "anger",   "💢": "anger",
    "🖕": "anger",
    # Hype / Enthousiasme
    "🔥": "hype",    "🚀": "hype",    "⚡": "hype",    "💥": "hype",
    "🎉": "hype",    "🏆": "hype",    "💪": "hype",    "😍": "hype",
    "🤩": "hype",    "👑": "hype",
    # Humour
    "😂": "humor",   "🤣": "humor",   "😹": "humor",   "😆": "humor",
    "🙃": "humor",   "😜": "humor",
    # Solidarité
    "❤️": "solidarity", "🤝": "solidarity", "🙏": "solidarity",
    "💙": "solidarity", "💚": "solidarity", "🫂": "solidarity",
    "🕊️": "solidarity",
    # Panique / Peur
    "😨": "panic",   "😱": "panic",   "😰": "panic",   "🆘": "panic",
    "⚠️": "panic",   "🚨": "panic",   "😧": "panic",
}

# Mots-clés français par émotion
FRENCH_KEYWORDS: dict[str, list[str]] = {
    "sadness": [
        "mort", "décès", "deuil", "tragédie", "triste", "tristesse",
        "perdu", "perte", "victime", "catastrophe", "sinistre", "drame",
        "enterrement", "funérailles", "condoléances", "blessé", "disparu",
    ],
    "anger": [
        "scandale", "honte", "inacceptable", "révoltant", "inadmissible",
        "corruption", "injustice", "abus", "criminel", "voleur", "menteur",
        "incompétent", "trahison", "colère", "boycott", "manifestation",
        "protestation", "grève", "dénonce",
    ],
    "hype": [
        "incroyable", "fantastique", "exceptionnel", "viral", "tendance",
        "buzz", "record", "succès", "victoire", "champion", "exploit",
        "magnifique", "époustouflant", "révolution", "innovation", "bravo",
        "félicitations", "génial", "top",
    ],
    "humor": [
        "lol", "mdr", "ptdr", "rigolo", "drôle", "blague", "hilarant",
        "comique", "farce", "humour", "rire", "rigoler", "marrant",
    ],
    "solidarity": [
        "solidarité", "ensemble", "soutien", "aide", "entraide", "don",
        "bénévolat", "communauté", "union", "partage", "compassion",
        "fraternité", "aidons", "soutenons", "prière",
    ],
    "panic": [
        "urgent", "danger", "alerte", "panique", "catastrophe", "urgence",
        "fuite", "évacuation", "incendie", "accident", "explosion", "attentat",
        "séisme", "inondation", "mort imminent", "sos", "au secours",
        "critique", "grave", "immédiat",
    ],
}

# Mots-clés arabe/darija par émotion
ARABIC_DARIJA_KEYWORDS: dict[str, list[str]] = {
    "sadness": [
        "موت", "وفاة", "حزن", "كارثة", "ضحايا", "مصيبة",
        "حزين", "بكا", "فقدان", "ألم",                   # Arabe standard
        "برشا حزن", "تعبان", "miskine", "barcha",         # Darija
    ],
    "anger": [
        "غضب", "فضيحة", "سرقة", "ظلم", "حرام", "خيانة",
        "عيب", "مسخرة", "يسرق", "فاسد",                  # Arabe standard
        "3ayb", "hchouma", "maandhomch", "haram",          # Darija latinisée
    ],
    "hype": [
        "رائع", "ممتاز", "نجاح", "بطولة", "انجاز", "فخر",
        "عظيم", "متميز",                                   # Arabe standard
        "top", "3azhim", "behi barcha", "yaaser",           # Darija
    ],
    "humor": [
        "مضحك", "نكتة", "هاها", "روحك", "تفضحني",
        "hajja", "ndhak", "barcha dhok",                    # Darija
    ],
    "solidarity": [
        "دعم", "مساعدة", "تضامن", "معك", "ندعم",
        "نعاونو", "na3awnou", "maak", "solidarité",         # Darija
    ],
    "panic": [
        "خطر", "نجدة", "فزعة", "عاجل", "حريق", "هروب",
        "كارثة", "انفجار", "زلزال",                        # Arabe standard
        "najda", "khatar", "3ajil", "hasla kathartha",      # Darija
    ],
}

# Poids relatifs pour le calcul du score (somme = 1.0)
WEIGHT_EMOJI:    float = 0.45
WEIGHT_FRENCH:   float = 0.35
WEIGHT_ARABIC:   float = 0.20


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

def extract_emojis(text: str) -> list[str]:
    """
    Extrait tous les emojis distincts présents dans le texte.

    Args:
        text : texte brut (post social)

    Returns:
        liste d'emojis trouvés (ex: ["😢", "🔥"])
    """
    if not text:
        return []
    # emoji_lib.emoji_list retourne [{"emoji": "🔥", "match_start": ..., "match_end": ...}]
    found = emoji_lib.emoji_list(text)
    return list(dict.fromkeys(e["emoji"] for e in found))  # dédupliqué, ordre préservé


def _score_emojis(emojis: list[str]) -> tuple[str | None, float]:
    """
    Calcule l'émotion dominante et son score brut depuis les emojis.

    Returns:
        (emotion_dominante | None, score_brut 0.0-1.0)
    """
    if not emojis:
        return None, 0.0

    # Compte les émotions représentées par les emojis détectés
    emotion_counts: dict[str, int] = {}
    for em in emojis:
        emotion = EMOJI_EMOTION_MAP.get(em)
        if emotion:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    if not emotion_counts:
        return None, 0.0

    # Émotion avec le plus d'emojis
    dominant = max(emotion_counts, key=emotion_counts.get)
    # Score brut : proportion d'emojis "signifiants" * force du signal
    total_mapped = sum(emotion_counts.values())
    raw_score = min(1.0, total_mapped / max(len(emojis), 1))

    return dominant, raw_score


def _score_keywords(text: str, lang: str = "french") -> tuple[str | None, float]:
    """
    Calcule l'émotion dominante depuis les mots-clés (FR ou AR/Darija).

    Args:
        text : texte normalisé
        lang : "french" | "arabic"

    Returns:
        (emotion_dominante | None, score_brut 0.0-1.0)
    """
    lexicon = FRENCH_KEYWORDS if lang == "french" else ARABIC_DARIJA_KEYWORDS
    emotion_counts: dict[str, int] = {}

    for emotion, keywords in lexicon.items():
        found = extract_keywords(text, keywords)
        if found:
            emotion_counts[emotion] = len(found)

    if not emotion_counts:
        return None, 0.0

    dominant = max(emotion_counts, key=emotion_counts.get)
    # Normalise : 1 mot = 0.3, 2 mots = 0.6, 3+ mots = 0.9+
    raw_score = min(1.0, emotion_counts[dominant] * 0.3)

    return dominant, raw_score


def detect_emotion(text: str) -> dict:
    """
    Détecte l'émotion dominante d'un texte en combinant :
      - emojis (poids 45%)
      - mots-clés français (poids 35%)
      - mots-clés arabe/darija (poids 20%)

    Args:
        text : texte brut du post

    Returns:
        {
            "emotion": str,   # émotion dominante
            "secondary_emotion": str | None,
            "score": int,      # confiance 0-100
            "confidence_index": int
        }
    """
    if not text or not text.strip():
        return {
            "emotion": "neutral",
            "secondary_emotion": "neutral",
            "score": 0,
            "confidence_index": 0,
        }

    # ── Analyse par couche ────────────────────────────────
    emojis        = extract_emojis(text)
    em_emoji,  s_emoji  = _score_emojis(emojis)
    em_fr,     s_fr     = _score_keywords(text, "french")
    em_ar,     s_ar     = _score_keywords(text, "arabic")

    # ── Vote pondéré ──────────────────────────────────────
    votes: dict[str, float] = {}

    if em_emoji:
        votes[em_emoji] = votes.get(em_emoji, 0) + s_emoji * WEIGHT_EMOJI
    if em_fr:
        votes[em_fr]    = votes.get(em_fr, 0)    + s_fr    * WEIGHT_FRENCH
    if em_ar:
        votes[em_ar]    = votes.get(em_ar, 0)    + s_ar    * WEIGHT_ARABIC

    if not votes:
        return {
            "emotion": "neutral",
            "secondary_emotion": "neutral",
            "score": 0,
            "confidence_index": 0,
        }

    # ── Émotion gagnante ──────────────────────────────────
    ranked_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
    dominant_emotion = ranked_votes[0][0]
    secondary_emotion = ranked_votes[1][0] if len(ranked_votes) > 1 else None
    raw_confidence   = ranked_votes[0][1]          # 0.0 → ~1.0
    secondary_score  = ranked_votes[1][1] if len(ranked_votes) > 1 else 0.0

    # Normalise vers 0-100 (max théorique = 1.0 si toutes les couches s'accordent)
    score = normalize_score(raw_confidence, 0.0, 1.0)
    confidence_index = normalize_score(
        (raw_confidence + max(raw_confidence - secondary_score, 0.0)) / 2,
        0.0,
        1.0,
    )

    return {
        "emotion": dominant_emotion,
        "secondary_emotion": secondary_emotion,
        "score": score,
        "confidence_index": score,
    }


def analyze_post(post: dict) -> dict:
    """
    Analyse complète d'un post : émotion + emojis.
    Entrée principale utilisée par process_post() dans fake_detector.py.

    Args:
        post : {
            "content" : str,           # texte du post (obligatoire)
            "region"  : str,           # ex: "Sfax" (optionnel)
            ...autres champs...
        }

    Returns:
        post enrichi avec :
            "emotion"       : str (sadness/anger/hype/humor/solidarity/panic/neutral)
            "emotion_score" : int 0-100
            "emojis"        : list[str]
    """
    content = post.get("content", "")
    cleaned = clean_text(content)

    # Extraction emojis sur texte brut (avant nettoyage qui pourrait les affecter)
    emojis_found = extract_emojis(content)

    # Détection émotion
    result = detect_emotion(cleaned)

    return {
        **post,
        "emotion":       result["emotion"],
        "emotion_score": result["score"],
        "secondary_emotion": result.get("secondary_emotion", "neutral"),
        "confidence_index": result.get("confidence_index", result.get("score", 0)),
        "emojis":        emojis_found,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TEST AUTONOME
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("TEST — emotion_analyzer.py")
    print("=" * 60)

    test_posts = [
        {
            "content": "😡😡 Scandale incroyable à Tunis ! Corruption partout, honte à ce gouvernement !!",
            "region": "Tunis",
            "source": "Facebook Group Tunis"
        },
        {
            "content": "😢💔 Condoléances à la famille de la victime. Triste journée pour Sfax.",
            "region": "Sfax",
            "source": "Médias locaux"
        },
        {
            "content": "🔥🚀🎉 Record battu ! L'équipe tunisienne est championne ! Incroyable exploit !",
            "region": "National",
            "source": "TikTok"
        },
        {
            "content": "🚨⚠️ URGENT : Incendie grave à Gabès ! Fuite immédiate recommandée ! Catastrophe !",
            "region": "Gabès",
            "source": "Facebook Group Gabès"
        },
        {
            "content": "😂😂 Mdr cette vidéo est trop hilarante, je peux pas arrêter de rire lol",
            "region": "Sousse",
            "source": "TikTok"
        },
        {
            "content": "❤️🤝 Solidarité avec les victimes des inondations. Ensemble nous sommes plus forts. Don urgent.",
            "region": "Nabeul",
            "source": "ONG Tunisie"
        },
        {
            "content": "فضيحة كبيرة ! غضب في الشارع التونسي بسبب الفساد 😤",
            "region": "Tunis",
            "source": "Twitter"
        },
        {
            "content": "",
            "region": "Unknown",
            "source": "Unknown"
        },
    ]

    for i, post in enumerate(test_posts, 1):
        result = analyze_post(post)
        print(f"\n[Post {i}] {post['region']} | {post['source']}")
        print(f"  Contenu  : {post['content'][:60]}...")
        print(f"  Émotion  : {result['emotion']} (score: {result['emotion_score']})")
        print(f"  Emojis   : {result['emojis']}")

    print("\n" + "=" * 60)
    print("✅ Tests emotion_analyzer.py terminés")
    print("=" * 60)